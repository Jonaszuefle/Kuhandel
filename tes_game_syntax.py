from game.player_view import PlayerView, PublicView

    

if __name__ == "__main__":
    a = PlayerView(0, [PublicView(0, "as", [10], 1, 20), PublicView(1, "q68er", [10], 1, 20)], None)

    max_len = max(len(name.player_name) for name in a.public)

    print(max_len)

    for pub in a.public:
        print(pub.player_name)


