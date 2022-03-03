#include "Move.hpp"

#include <ostream>
#include <optional>

Move::Move(const Square& from, const Square& to,
           const std::optional<PieceType>& promotion)
{
    from_ = from;
    to_ = to;
    promotion_ = promotion;
}

Move::Optional Move::fromUci(const std::string& uci) {
    char from_col = uci.at(0);
    char from_row = uci.at(1);
    char to_col = uci.at(2);
    char to_row = uci.at(3);

    int from_col_int = 0;

    if (from_col == 'a') {
        from_col_int = 0;
    }
    if (from_col == 'b') {
        from_col_int = 1;
    }
    if (from_col == 'c') {
        from_col_int = 2;
    }
    if (from_col == 'd') {
        from_col_int = 3;
    }
    if (from_col == 'e') {
        from_col_int = 4;
    }
    if (from_col == 'f') {
        from_col_int = 5;
    }
    if (from_col == 'g') {
        from_col_int = 6;
    }
    if (from_col == 'h') {
        from_col_int = 7;
    }

    from_row = from_row -1;
    to_row = to_row-1;

    Index from_index = from_col_int + 8*from_row;
    Index to_index = to_col + 8*to_row;

    Square from_Square = Square::fromIndex(from_index);
    Square to_Square = Square::fromIndex(to_index);

    Move move = Move(from_Square, to_Square);
    
    return move;
}

Square Move::from() const {
    return from_;
}

Square Move::to() const {
    return to_;
}

std::optional<PieceType> Move::promotion() const {
    return promotion_;
}

std::ostream& operator<<(std::ostream& os, const Move& move) {
    (void)move;
    return os;
}


bool operator<(const Move& lhs, const Move& rhs) {
    (void)lhs;
    (void)rhs;
    return false;
}

bool operator==(const Move& lhs, const Move& rhs) {
    (void)lhs;
    (void)rhs;
    return false;
}
