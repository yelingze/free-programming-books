class DiamondPattern:
    def __init__(self, size):
        if size <= 0 or size % 2 == 0:
            raise ValueError("Size must be a positive odd integer.")
        self.size = size

    def print_hollow_diamond(self):
        """Prints a hollow diamond pattern."""
        n = self.size
        mid = n // 2

        # Upper half including the middle row
        for i in range(mid + 1):
            spaces_before = ' ' * (mid - i)
            if i == 0:
                # First row: single star
                stars = '*'
            else:
                # Other rows: star, spaces, star
                spaces_inside = ' ' * (2 * i - 1)
                stars = '*' + spaces_inside + '*'
            print(spaces_before + stars)

        # Lower half
        for i in range(mid - 1, -1, -1):
            spaces_before = ' ' * (mid - i)
            if i == 0:
                # Last row: single star
                stars = '*'
            else:
                # Other rows: star, spaces, star
                spaces_inside = ' ' * (2 * i - 1)
                stars = '*' + spaces_inside + '*'
            print(spaces_before + stars)

    def print_filled_diamond(self):
        """Prints a filled diamond pattern."""
        n = self.size
        mid = n // 2

        # Upper half including the middle row
        for i in range(mid + 1):
            spaces_before = ' ' * (mid - i)
            stars = '*' * (2 * i + 1)
            print(spaces_before + stars)

        # Lower half
        for i in range(mid - 1, -1, -1):
            spaces_before = ' ' * (mid - i)
            stars = '*' * (2 * i + 1)
            print(spaces_before + stars)

# Example usage
if __name__ == "__main__":
    try:
        diamond = DiamondPattern(7)
        print("Hollow Diamond:")
        diamond.print_hollow_diamond()
        print("\nFilled Diamond:")
        diamond.print_filled_diamond()
        
        print("\n--- Using size 5 ---")
        diamond2 = DiamondPattern(5)
        print("Hollow Diamond:")
        diamond2.print_hollow_diamond()
        print("\nFilled Diamond:")
        diamond2.print_filled_diamond()
        
    except ValueError as e:
        print(f"Error: {e}")