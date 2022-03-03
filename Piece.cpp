#include "Piece.hpp"

#include <string>

#include <ostream>

Piece::Piece(PieceColor color, PieceType type)
{
    color_ = color;
    type_ = type;

    // (void)color;
    // (void)type;
}

Piece::Optional Piece::fromSymbol(char symbol) {
    if (symbol == 'P') {
        Piece newpiece = Piece(PieceColor::White, PieceType::Pawn);
        return newpiece;
    }
    if (symbol == 'R') {
        Piece newpiece = Piece(PieceColor::White, PieceType::Rook);
        return newpiece;
    }
    if (symbol == 'B') {
        Piece newpiece = Piece(PieceColor::White, PieceType::Bishop);
        return newpiece;
    }
    if (symbol == 'N') {
        Piece newpiece = Piece(PieceColor::White, PieceType::Knight);
        return newpiece;
    }
    if (symbol == 'K') {
        Piece newpiece = Piece(PieceColor::White, PieceType::King);
        return newpiece;
    }
    if (symbol == 'Q') {
        Piece newpiece = Piece(PieceColor::White, PieceType::Queen);
        return newpiece;
    }
    if (symbol == 'p') {
        Piece newpiece = Piece(PieceColor::Black, PieceType::Pawn);
        return newpiece;
    }
    if (symbol == 'r') {
        Piece newpiece = Piece(PieceColor::Black, PieceType::Rook);
        return newpiece;
    }
    if (symbol == 'b') {
        Piece newpiece = Piece(PieceColor::Black, PieceType::Bishop);
        return newpiece;
    }
    if (symbol == 'n') {
        Piece newpiece = Piece(PieceColor::Black, PieceType::Knight);
        return newpiece;
    }
    if (symbol == 'k') {
        Piece newpiece = Piece(PieceColor::Black, PieceType::King);
        return newpiece;
    }
    if (symbol == 'q') {
        Piece newpiece = Piece(PieceColor::Black, PieceType::Queen);
        return newpiece;
    }

    // Piece piece = new Piece;
    // piece.color = PieceType color;

    // return std::nullopt;
}

PieceColor Piece::color() const {
    return color_;
}

PieceType Piece::type() const {
    return type_;
}

bool operator==(const Piece& lhs, const Piece& rhs) {
    if ((lhs.color() == rhs.color()) && (lhs.type() == rhs.type())) {
        return true;
    }
    else {
        return false;
    }
}

std::ostream& operator<<(std::ostream& os, const Piece& piece) {
    if (piece.color() == PieceColor::White) {
        if (piece.type() == PieceType::Pawn) {
            return os<<"P";
        }
        if (piece.type() == PieceType::Rook) {
            return os<<"R";
        }
        if (piece.type() == PieceType::Bishop) {
            return os<<"B";
        }
        if (piece.type() == PieceType::Knight) {
            return os<<"N";
        }
        if (piece.type() == PieceType::King) {
            return os<<"K";
        }
        if (piece.type() == PieceType::Queen) {
            return os<<"Q";
        }
    }

    else {
        if (piece.type() == PieceType::Pawn) {
            return os<<"p";
        }
        if (piece.type() == PieceType::Rook) {
            return os<<"r";
        }
        if (piece.type() == PieceType::Bishop) {
            return os<<"b";
        }
        if (piece.type() == PieceType::Knight) {
            return os<<"n";
        }
        if (piece.type() == PieceType::King) {
            return os<<"k";
        }
        if (piece.type() == PieceType::Queen) {
            return os<<"q";
        }
    }
}

PieceColor operator!(PieceColor color) {
    if (color == PieceColor::Black) {
        return PieceColor::White;
    }
    else {
        return PieceColor::Black;
    }
}
