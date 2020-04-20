if __name__ == "__main__":
    from listing_obtainers.TSXObtainer import TSXObtainer

    obtainer = TSXObtainer()
    df = obtainer.obtain()
    print("Yay")
