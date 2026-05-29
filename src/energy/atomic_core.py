class AtomicCore:
    def __init__(self):
        self.precision = 1.0
        self.surprise = 0.0
        print("AtomicCore initialized.")

    def calculate_energy(self, input_data):
        # Thermodynamic baseline calculation
        self.surprise = abs(len(str(input_data)) * 0.01)
        return self.surprise

    def reset(self):
        self.surprise = 0.0
