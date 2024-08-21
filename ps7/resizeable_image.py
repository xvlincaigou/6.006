import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    class node:
        def __init__(self, total_energy, direction=None) -> None:
            self.total_energy = total_energy
            self.direction = direction

    def best_seam(self):
        w = self.width
        h = self.height
        energy_nodes = [[self.energy(i, j) for i in range(w)] for j in range(h)]
        total_energy_nodes = [[(0, 0) for _ in range(w)] for _ in range(h)]
        
        # Initialize the bottom row
        for j in range(w):
            total_energy_nodes[h - 1][j] = (energy_nodes[h - 1][j], 0)

        # Fill the total_energy_nodes array
        for i in range(h - 2, -1, -1):
            for j in range(w):
                if j == 0:
                    direction = 0 if total_energy_nodes[i + 1][j][0] <= total_energy_nodes[i + 1][j + 1][0] else 1
                elif j == w - 1:
                    direction = 0 if total_energy_nodes[i + 1][j][0] <= total_energy_nodes[i + 1][j - 1][0] else -1
                else:
                    min_energy = min(total_energy_nodes[i + 1][j - 1][0], total_energy_nodes[i + 1][j][0], total_energy_nodes[i + 1][j + 1][0])
                    if min_energy == total_energy_nodes[i + 1][j - 1][0]:
                        direction = -1
                    elif min_energy == total_energy_nodes[i + 1][j][0]:
                        direction = 0
                    else:
                        direction = 1
                total_energy_nodes[i][j] = (energy_nodes[i][j] + total_energy_nodes[i + 1][j + direction][0], direction)

        # Find the minimum energy in the top row
        min_energy = float('inf')
        min_index = 0
        for j in range(w):
            if total_energy_nodes[0][j][0] < min_energy:
                min_energy = total_energy_nodes[0][j][0]
                min_index = j

        # Reconstruct the seam path
        seam = [(0, min_index)]
        for i in range(h - 1):
            min_index += total_energy_nodes[i][min_index][1]
            seam.append((i + 1, min_index))

        return seam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())