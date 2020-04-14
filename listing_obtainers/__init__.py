from listing_obtainers.TSXObtainer import TSXObtainer

if __name__ == "__main__":
    obtainer = TSXObtainer()
    df = obtainer.obtain()
    print("Yay")
