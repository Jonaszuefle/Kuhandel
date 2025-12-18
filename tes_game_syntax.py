from game.player_view import PlayerView, PublicView


if __name__ == "__main__":
    a = PlayerView(
        0, [PublicView(0, "as", [10], 1, 20), PublicView(1, "q68er", [10], 1, 20)], None
    )

    max_len = max(len(name.player_name) for name in a.public)

    print(max_len)

    for pub in a.public:
        print(pub.player_name)

    x = [1,2,3]
    z = [3,4,5]

    print([x+z for x,z in zip(x,z)])
    
    player_names = ["Alice", "Bob", "Charlie", "David"]
    name_to_idx = {
        name.lower(): idx for idx, name in zip(range(len(player_names)), player_names)
    }

    print(name_to_idx)

    print(player_names.index("Charlie"))
