if __name__ == "__main__":
    from listing_obtainers.TSXListingObtainer import TSXListingObtainer

    obtainer = TSXListingObtainer()
    df = obtainer.obtain()
    print("Yay")
