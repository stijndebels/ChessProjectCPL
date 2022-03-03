#!/usr/bin/env python3

from puzzledb import Puzzle, PuzzleDb

from pathlib import Path
import argparse
from abc import ABC, abstractmethod
from collections import defaultdict
import sys
import time
import asyncio
import contextlib

import chess
import chess.engine

import junit_xml
from junit_xml import TestSuite, TestCase


class PuzzleRunResult(ABC):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.puzzle_type = None
        self.duration_sec = None

    @abstractmethod
    def is_success(self):
        pass

    def to_junit_test_case(self):
        return TestCase(
            name=f'Puzzle {self.puzzle.puzzle_id}',
            status='run',
            classname=self.puzzle_type,
            elapsed_sec=self.duration_sec
        )


class PuzzleRunSuccess(PuzzleRunResult):
    def __init__(self, puzzle):
        super().__init__(puzzle)

    def is_success(self):
        return True


class PuzzleRunFailure(PuzzleRunResult):
    def __init__(self, puzzle, reason, info):
        super().__init__(puzzle)
        self.reason = reason
        url = f'https://lichess.org/training/{self.puzzle.puzzle_id}'
        self.info = f'URL: {url}\n{info}'

    def is_success(self):
        return False

    def __str__(self):
        return f'Failure reason: {self.reason}\n{self.info}'

    def to_junit_test_case(self):
        test_case = super().to_junit_test_case()
        test_case.add_failure_info(
            message=self.reason,
            output=self.info
        )

        return test_case


class PuzzleRunWrongMove(PuzzleRunFailure):
    def __init__(self, puzzle, position, move, expected_move):
        reason = 'unexpected move'
        info = f'position={position}\n' \
               f'move={move.uci()}\n' \
               f'expected move={expected_move.uci()}'

        super().__init__(puzzle, reason, info)


class PuzzleRunTimeout(PuzzleRunFailure):
    def __init__(self, puzzle, timeout):
        reason = 'timeout'
        info = f'Puzzle timed out after {timeout} seconds'
        super().__init__(puzzle, reason, info)


class PuzzleRunException(PuzzleRunFailure):
    def __init__(self, puzzle, exception):
        reason = 'exception'
        info = exception

        super().__init__(puzzle, reason, info)


@contextlib.asynccontextmanager
async def create_engine(engine_path):
    _, engine = await chess.engine.popen_uci(engine_path)

    try:
        yield engine
    finally:
        await engine.quit()


async def _run_puzzle(puzzle, engine_path):
    moves = puzzle.moves[:]
    assert len(moves) >= 2
    assert len(moves) % 2 == 0

    board = chess.Board(puzzle.fen)

    async with create_engine(engine_path) as engine:
        while len(moves) > 0:
            board.push(moves.pop(0))
            result = await engine.play(board, chess.engine.Limit())
            board.push(result.move)
            expected_move = moves.pop(0)

            if result.move != expected_move:
                if len(moves) == 0 and board.is_checkmate():
                    break
                else:
                    board.pop()
                    return PuzzleRunWrongMove(puzzle, board.fen(),
                                              result.move, expected_move)

    return PuzzleRunSuccess(puzzle)


def run_puzzle(puzzle, engine_path, timeout):
    async def run():
        try:
            return await asyncio.wait_for(
                _run_puzzle(puzzle, engine_path),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return PuzzleRunTimeout(puzzle, timeout)
        except Exception as e:
            return PuzzleRunException(puzzle, e)

    start_time = time.time()
    result = asyncio.run(run())
    end_time = time.time()
    result.duration_sec = end_time - start_time
    return result


def format_duration(duration):
    return f'{duration:.3f}s'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--timeout', type=float,
                        help='Timeout in seconds per puzzle')
    parser.add_argument('--junit', type=Path)
    parser.add_argument('puzzle_dbs', type=Path, nargs='+')
    args = parser.parse_args()

    results = defaultdict(list)
    num_fails = 0
    total_duration = 0

    for puzzle_db_path in args.puzzle_dbs:
        print(f'=== Running puzzles from {puzzle_db_path.resolve()} ===')

        with puzzle_db_path.open(newline='') as f:
            puzzles = PuzzleDb.from_csv(f)

            for puzzle in puzzles:
                print(f'Running puzzle {puzzle.puzzle_id} ... ',
                      end='', flush=True)
                result = run_puzzle(puzzle, args.engine, args.timeout)
                total_duration += result.duration_sec
                duration_msg = f'({format_duration(result.duration_sec)})'

                if result.is_success():
                    print(f'OK {duration_msg}')
                else:
                    num_fails += 1
                    print(f'FAIL {duration_msg}')
                    print(f'===\n{result}\n===')

                results[puzzle_db_path].append(result)

        if args.junit is not None:
            test_suites = []

            for db_path, db_results in results.items():
                name = f'puzzles.{db_path.stem}'

                def create_test_case(result):
                    result.puzzle_type = name
                    return result.to_junit_test_case()

                test_cases = [create_test_case(r) for r in db_results]
                test_suite = TestSuite(name, test_cases)
                test_suites.append(test_suite)

            xml = junit_xml.to_xml_report_string(test_suites)
            args.junit.write_text(xml)

    print(f'Total time: {format_duration(total_duration)}')

    if num_fails > 0:
        sys.exit(f'{num_fails} tests failed')
    else:
        print('All tests passed')


if __name__ == '__main__':
    main()
