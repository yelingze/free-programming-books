class SortingAlgorithms:
    """A class containing various sorting algorithms."""

    def bubble_sort(self, arr):
        """
        Sorts an array using the bubble sort algorithm.

        Args:
            arr (list): A list of comparable elements.

        Returns:
            list: The sorted list.
        """
        n = len(arr)
        # Traverse through all array elements
        for i in range(n):
            # Flag to detect if any swap happens
            swapped = False
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # Traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            # If no two elements were swapped by inner loop, then break
            if not swapped:
                break
        return arr

# Example usage
if __name__ == "__main__":
    sorter = SortingAlgorithms()
    unsorted_list = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted list:", unsorted_list)
    sorted_list = sorter.bubble_sort(unsorted_list.copy())
    print("Sorted list:", sorted_list)
