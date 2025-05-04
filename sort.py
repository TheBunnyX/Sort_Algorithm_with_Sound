import tkinter as tk
import random
import winsound
import time

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualization and Audibilization")
        self.NUM_ELEMENTS = 50
        self.array = [i + 1 for i in range(self.NUM_ELEMENTS)]
        random.shuffle(self.array)
        self.max_value = max(self.array)
        self.comparisons = 0
        self.swaps = 0
        self.sorting = False
        self.stop = False  # Flag to indicate stop request
        self.delay = 0.05  # Delay for visualization and sound during sorting
        self.final_delay = 0.02  # Shorter delay for final sequence

        # Canvas setup
        self.WIDTH = 800
        self.HEIGHT = 400
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack(pady=10)
        self.bar_width = self.WIDTH // self.NUM_ELEMENTS

        # Labels
        self.algo_label = tk.Label(root, text="Algorithm: None")
        self.algo_label.pack()
        self.comp_label = tk.Label(root, text="Comparisons: 0")
        self.comp_label.pack()
        self.swap_label = tk.Label(root, text="Swaps: 0")
        self.swap_label.pack()

        # Buttons
        tk.Button(root, text="Bubble Sort", command=self.start_bubble_sort).pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Quick Sort", command=self.start_quick_sort).pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Selection Sort", command=self.start_selection_sort).pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Merge Sort", command=self.start_merge_sort).pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Insertion Sort", command=self.start_insertion_sort).pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Heap Sort", command=self.start_heap_sort).pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Stop", command=self.stop_sorting).pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=10)

        # Sound settings
        self.MIN_FREQ = 2000
        self.MAX_FREQ = 8000
        self.SOUND_DURATION = 20  # ms for crisper final sequence

        self.draw_array()

    def value_to_frequency(self, value):
        """Map array value to frequency for sound."""
        return int(self.MIN_FREQ + (self.MAX_FREQ - self.MIN_FREQ) * (value - 1) / (self.max_value - 1))

    def play_sound(self, value):
        """Play a beep for the given value."""
        freq = self.value_to_frequency(value)
        try:
            winsound.Beep(freq, self.SOUND_DURATION)
        except:
            pass  # Silently skip if sound fails (e.g., non-Windows OS)

    def play_final_sequence(self):
        """Play tones for all values from low to high after sorting."""
        if not self.stop:
            for i in range(len(self.array)):
                if self.stop:
                    break
                self.draw_array(list(range(i + 1)))  # Highlight all bars up to current index
                self.play_sound(self.array[i])
                time.sleep(self.final_delay)
            self.draw_array()  # Clear highlights

    def draw_array(self, highlight_indices=None):
        """Draw the array as bars, highlighting specified indices in red."""
        self.canvas.delete("all")
        for i, value in enumerate(self.array):
            color = "red" if highlight_indices and i in highlight_indices else "white"
            height = (value / self.max_value) * (self.HEIGHT - 50)
            self.canvas.create_rectangle(
                i * self.bar_width, self.HEIGHT - height,
                (i + 1) * self.bar_width - 2, self.HEIGHT,
                fill=color
            )
        self.comp_label.config(text=f"Comparisons: {self.comparisons}")
        self.swap_label.config(text=f"Swaps: {self.swaps}")
        self.root.update()

    def bubble_sort(self):
        """Bubble sort with visualization and sound."""
        n = len(self.array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if not self.sorting or self.stop:
                    break
                self.comparisons += 1
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.swaps += 1
                    self.play_sound(self.array[j])
                    self.draw_array([j, j + 1])
                    time.sleep(self.delay)
                else:
                    self.draw_array([j, j + 1])
                    time.sleep(self.delay)
            if not self.sorting or self.stop:
                break
        if self.sorting and not self.stop:
            self.play_final_sequence()
        self.sorting = False
        self.draw_array()

    def quick_sort(self, low, high):
        """Quick sort with visualization and sound."""
        def partition(low, high):
            if self.stop:
                return low  # Early exit
            pivot = self.array[high]
            i = low - 1
            for j in range(low, high):
                if self.stop:
                    break
                self.comparisons += 1
                if self.array[j] <= pivot:
                    i += 1
                    self.array[i], self.array[j] = self.array[j], self.array[i]
                    self.swaps += 1
                    self.play_sound(self.array[i])
                    self.draw_array([i, j, high])
                    time.sleep(self.delay)
            self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
            self.swaps += 1
            self.play_sound(self.array[i + 1])
            self.draw_array([i + 1, high])
            time.sleep(self.delay)
            return i + 1

        if low < high and self.sorting and not self.stop:
            pi = partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def selection_sort(self):
        """Selection sort with visualization and sound."""
        n = len(self.array)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if not self.sorting or self.stop:
                    break
                self.comparisons += 1
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
                self.draw_array([i, j, min_idx])
                time.sleep(self.delay)
            if not self.sorting or self.stop:
                break
            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self.swaps += 1
                self.play_sound(self.array[i])
                self.draw_array([i, min_idx])
                time.sleep(self.delay)
        if self.sorting and not self.stop:
            self.play_final_sequence()
        self.sorting = False
        self.draw_array()

    def merge_sort(self, low, high):
        """Merge sort with visualization and sound."""
        def merge(low, mid, high):
            if self.stop:
                return
            left = self.array[low:mid + 1]
            right = self.array[mid + 1:high + 1]
            i = j = 0
            k = low
            while i < len(left) and j < len(right):
                if self.stop:
                    break
                self.comparisons += 1
                if left[i] <= right[j]:
                    self.array[k] = left[i]
                    i += 1
                else:
                    self.array[k] = right[j]
                    j += 1
                self.swaps += 1
                self.play_sound(self.array[k])
                self.draw_array([k])
                time.sleep(self.delay)
                k += 1
            while i < len(left) and not self.stop:
                self.array[k] = left[i]
                self.swaps += 1
                self.play_sound(self.array[k])
                self.draw_array([k])
                time.sleep(self.delay)
                i += 1
                k += 1
            while j < len(right) and not self.stop:
                self.array[k] = right[j]
                self.swaps += 1
                self.play_sound(self.array[k])
                self.draw_array([k])
                time.sleep(self.delay)
                j += 1
                k += 1

        if low < high and self.sorting and not self.stop:
            mid = (low + high) // 2
            self.merge_sort(low, mid)
            self.merge_sort(mid + 1, high)
            merge(low, mid, high)

    def insertion_sort(self):
        """Insertion sort with visualization and sound."""
        n = len(self.array)
        for i in range(1, n):
            key = self.array[i]
            j = i - 1
            while j >= 0 and self.sorting and not self.stop:
                self.comparisons += 1
                if self.array[j] > key:
                    self.array[j + 1] = self.array[j]
                    self.swaps += 1
                    self.play_sound(self.array[j + 1])
                    self.draw_array([j, j + 1])
                    time.sleep(self.delay)
                    j -= 1
                else:
                    self.draw_array([j, j + 1])
                    time.sleep(self.delay)
                    break
            if not self.sorting or self.stop:
                break
            self.array[j + 1] = key
            self.swaps += 1
            self.play_sound(self.array[j + 1])
            self.draw_array([j + 1])
            time.sleep(self.delay)
        if self.sorting and not self.stop:
            self.play_final_sequence()
        self.sorting = False
        self.draw_array()

    def heap_sort(self):
        """Heap sort with visualization and sound."""
        def heapify(n, i):
            if self.stop:
                return
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and self.array[left] > self.array[largest]:
                self.comparisons += 1
                largest = left

            if right < n and self.array[right] > self.array[largest]:
                self.comparisons += 1
                largest = right

            if largest != i:
                self.array[i], self.array[largest] = self.array[largest], self.array[i]
                self.swaps += 1
                self.play_sound(self.array[i])
                self.draw_array([i, largest])
                time.sleep(self.delay)
                heapify(n, largest)

        n = len(self.array)
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            if not self.sorting or self.stop:
                break
            heapify(n, i)
        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            if not self.sorting or self.stop:
                break
            self.array[0], self.array[i] = self.array[i], self.array[0]
            self.swaps += 1
            self.play_sound(self.array[0])
            self.draw_array([0, i])
            time.sleep(self.delay)
            heapify(i, 0)
        if self.sorting and not self.stop:
            self.play_final_sequence()
        self.sorting = False
        self.draw_array()

    def start_bubble_sort(self):
        """Start bubble sort if not already sorting."""
        if not self.sorting:
            self.sorting = True
            self.stop = False
            self.algo_label.config(text="Algorithm: Bubble Sort")
            self.bubble_sort()

    def start_quick_sort(self):
        """Start quick sort if not already sorting."""
        if not self.sorting:
            self.sorting = True
            self.stop = False
            self.algo_label.config(text="Algorithm: Quick Sort")
            self.quick_sort(0, len(self.array) - 1)
            if self.sorting and not self.stop:
                self.play_final_sequence()
            self.sorting = False
            self.draw_array()

    def start_selection_sort(self):
        """Start selection sort if not already sorting."""
        if not self.sorting:
            self.sorting = True
            self.stop = False
            self.algo_label.config(text="Algorithm: Selection Sort")
            self.selection_sort()

    def start_merge_sort(self):
        """Start merge sort if not already sorting."""
        if not self.sorting:
            self.sorting = True
            self.stop = False
            self.algo_label.config(text="Algorithm: Merge Sort")
            self.merge_sort(0, len(self.array) - 1)
            if self.sorting and not self.stop:
                self.play_final_sequence()
            self.sorting = False
            self.draw_array()

    def start_insertion_sort(self):
        """Start insertion sort if not already sorting."""
        if not self.sorting:
            self.sorting = True
            self.stop = False
            self.algo_label.config(text="Algorithm: Insertion Sort")
            self.insertion_sort()

    def start_heap_sort(self):
        """Start heap sort if not already sorting."""
        if not self.sorting:
            self.sorting = True
            self.stop = False
            self.algo_label.config(text="Algorithm: Heap Sort")
            self.heap_sort()

    def stop_sorting(self):
        """Stop the current sorting process."""
        if self.sorting:
            self.stop = True
            self.sorting = False
            self.algo_label.config(text="Algorithm: None")
            self.draw_array()

    def reset(self):
        """Reset the array and counters."""
        random.shuffle(self.array)
        self.comparisons = 0
        self.swaps = 0
        self.sorting = False
        self.stop = False
        self.algo_label.config(text="Algorithm: None")
        self.draw_array()

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()