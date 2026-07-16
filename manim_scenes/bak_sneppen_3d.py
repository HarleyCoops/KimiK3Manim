"""
Bak-Sneppen Model 3D Visualization
====================================

A comprehensive Manim implementation showcasing self-organized criticality
through evolutionary avalanches in a rotating 3D environment.

Author: Math-To-Manim Project
License: MIT
"""

from manim import *
import numpy as np
import random

class BakSneppenEvolution3D(ThreeDScene):
    """
    Main 3D visualization scene for the Bak-Sneppen evolutionary model.
    
    Features:
    - Rotating 3D camera perspective
    - Species represented as colored spheres with vertical fitness bars
    - Real-time fitness distribution graph
    - Animated avalanche cascades
    - Iteration counter and UI elements
    - Mathematical summary finale
    """
    
    # Configuration parameters
    NUM_SPECIES = 30          # Number of species in the circle
    RADIUS = 4                 # Radius of species circle
    SPHERE_RADIUS = 0.25       # Size of each species sphere
    NUM_ITERATIONS = 50        # Simulation steps to show
    ANIMATION_SPEED = 0.5      # Seconds per iteration
    BAR_MAX_HEIGHT = 2.0       # Maximum height of fitness bars
    
    def construct(self):
        """Main orchestration method."""
        # Set up 3D environment
        self.setup_camera()
        
        # Create scene elements
        title = self.create_title()
        species_vgroup, fitness_values = self.initialize_species()
        graph_axes, bars = self.create_fitness_graph(fitness_values)
        iteration_label = self.create_iteration_counter()
        
        # Arrange layout
        self.add_fixed_in_frame_mobjects(title, iteration_label)
        title.to_corner(UL)
        iteration_label.to_corner(UR)
        
        # Initial animation
        self.play(Write(title), Write(iteration_label))
        self.play(
            LaggedStart(
                *[Create(sphere) for sphere in species_vgroup],
                lag_ratio=0.05
            ),
            run_time=2
        )
        self.wait(0.5)
        
        # Run simulation
        self.run_simulation(
            species_vgroup, 
            fitness_values, 
            graph_axes, 
            bars, 
            iteration_label
        )
        
        # Finale
        self.finale()
    
    def setup_camera(self):
        """Configure 3D camera for optimal viewing."""
        self.set_camera_orientation(
            phi=60 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.8
        )
        # Start with a static view, we will rotate later
    
    def create_title(self):
        """Create animated title with gradient effect."""
        title = Text(
            "Bak-Sneppen Evolutionary Model", 
            font_size=36,
            weight=BOLD
        )
        title.set_color_by_gradient(BLUE, GREEN)
        return title
    
    def initialize_species(self):
        """
        Create initial species arrangement in a circle.
        
        Returns:
            species_vgroup: VGroup of all species objects
            fitness_values: List of current fitness values
        """
        self.species_objects = []
        fitness_values = []
        
        for i in range(self.NUM_SPECIES):
            # Calculate position in circle
            angle = 2 * np.pi * i / self.NUM_SPECIES
            x = self.RADIUS * np.cos(angle)
            y = self.RADIUS * np.sin(angle)
            
            # Generate random fitness
            fitness = random.random()
            fitness_values.append(fitness)
            
            # Create sphere representation
            color = self.fitness_to_color(fitness)
            sphere = Sphere(
                center=(x, y, 0),
                radius=self.SPHERE_RADIUS,
                resolution=(16, 16),
                color=color
            )
            
            # Create vertical fitness bar
            bar_height = fitness * self.BAR_MAX_HEIGHT
            bar = Cylinder(
                radius=self.SPHERE_RADIUS * 0.6,
                height=bar_height,
                color=color,
                resolution=(8, 8)
            )
            bar.move_to([x, y, bar_height / 2])
            
            # Add index label
            label = Text(str(i), font_size=16, color=WHITE)
            label.move_to([x, y, -0.5])
            
            # Group elements
            species_group = VGroup(sphere, bar, label)
            self.species_objects.append({
                'sphere': sphere,
                'bar': bar,
                'label': label,
                'group': species_group,
                'index': i
            })
        
        # Create main VGroup
        species_vgroup = VGroup(*[obj['group'] for obj in self.species_objects])
        
        return species_vgroup, fitness_values
    
    def fitness_to_color(self, fitness):
        """
        Map fitness value to color gradient (red=0, green=1).
        
        Args:
            fitness: Float between 0 and 1
            
        Returns:
            Manim color object
        """
        return interpolate_color(RED, GREEN, fitness)
    
    def create_fitness_graph(self, fitness_values):
        """
        Create real-time fitness distribution graph.
        
        Args:
            fitness_values: Initial list of fitness values
            
        Returns:
            axes: Graph axes
            bars: BarChart object
        """
        # Create axes with smaller size
        axes = Axes(
            x_range=[0, self.NUM_SPECIES, 5],
            y_range=[0, 1, 0.2],
            x_length=5,
            y_length=2.5,
            axis_config={"include_tip": False},
            tips=False
        )
        
        # Position in bottom left corner, but with safe margin
        # Frame bottom is approx -4, left is -7.1
        axes.to_corner(DL, buff=1.0)
        
        # Create bar chart
        bars = BarChart(
            values=fitness_values,
            bar_names=[str(i) for i in range(self.NUM_SPECIES)],
            y_range=[0, 1, 0.2],
            x_length=4.5, # Slightly smaller than axes to fit inside
            y_length=2.3,
            bar_width=0.12,
            bar_colors=[self.fitness_to_color(f) for f in fitness_values]
        )
        # Align bars to axes
        bars.move_to(axes.get_center())
        
        # Add labels
        x_label = Text("Species Index", font_size=16)
        y_label = Text("Fitness", font_size=16)
        x_label.next_to(axes, DOWN, buff=0.2)
        y_label.next_to(axes, LEFT, buff=0.2).rotate(PI/2)
        
        graph_group = VGroup(axes, bars, x_label, y_label)
        self.add_fixed_in_frame_mobjects(graph_group)
        
        # Store axes center for updates
        self.graph_center = axes.get_center()
        
        return axes, bars
    
    def create_iteration_counter(self):
        """Create iteration counter display."""
        counter = Text("Iteration: 0", font_size=24, color=YELLOW)
        return counter
    
    def run_simulation(self, species_vgroup, fitness_values, graph_axes, bars, iteration_label):
        """
        Execute Bak-Sneppen dynamics with animations.
        
        Args:
            species_vgroup: VGroup of all species
            fitness_values: List of current fitness values
            graph_axes: Graph axes object
            bars: BarChart object
            iteration_label: Iteration counter display
        """
        for iteration in range(self.NUM_ITERATIONS):
            # Find species with minimum fitness
            min_idx = fitness_values.index(min(fitness_values))
            neighbors = [
                (min_idx - 1) % self.NUM_SPECIES,
                min_idx,
                (min_idx + 1) % self.NUM_SPECIES
            ]
            
            # Camera control: Zoom in on the first avalanche
            if iteration == 1:
                # self.stop_ambient_camera_rotation() # Not started yet
                target_species = self.species_objects[min_idx]['sphere']
                self.move_camera(
                    zoom=1.5,
                    frame_center=target_species.get_center(),
                    run_time=1.5
                )
            
            # Camera control: Zoom out after a few iterations
            if iteration == 3:
                self.move_camera(
                    zoom=0.8,
                    frame_center=ORIGIN,
                    run_time=1.5
                )
                self.begin_ambient_camera_rotation(rate=0.1)
            
            # Highlight the avalanche
            self.highlight_species(min_idx, neighbors)
            
            # Replace species with new random fitness values
            self.replace_species(min_idx, neighbors, fitness_values)
            
            # Update visualizations
            self.update_fitness_graph(bars, fitness_values)
            self.update_iteration_counter(iteration_label, iteration + 1)
            
            # Brief pause to show the change
            self.wait(self.ANIMATION_SPEED)
            
            # Remove highlights
            self.remove_highlights(neighbors)
    
    def highlight_species(self, center_idx, neighbor_indices):
        """
        Emphasize species involved in avalanche.
        
        Args:
            center_idx: Index of minimum fitness species
            neighbor_indices: List of all affected indices
        """
        # Create pulsing rings around affected species
        self.highlight_rings = VGroup()
        
        for idx in neighbor_indices:
            obj = self.species_objects[idx]
            ring = Circle(
                radius=self.SPHERE_RADIUS * 1.8,
                color=YELLOW,
                stroke_width=3
            )
            ring.move_to(obj['sphere'].get_center())
            self.highlight_rings.add(ring)
        
        self.play(Create(self.highlight_rings), run_time=0.3)
        
        # Pulse the central species
        central_obj = self.species_objects[center_idx]
        self.play(
            central_obj['sphere'].animate.scale(1.5),
            rate_func=there_and_back,
            run_time=0.3
        )
    
    def replace_species(self, center_idx, neighbor_indices, fitness_values):
        """
        Animate replacement of species with new fitness values.
        
        Args:
            center_idx: Center of avalanche
            neighbor_indices: All species to replace
            fitness_values: List to update
        """
        animations = []
        
        for idx in neighbor_indices:
            # Generate new fitness
            new_fitness = random.random()
            old_fitness = fitness_values[idx]
            
            # Update stored value
            fitness_values[idx] = new_fitness
            
            # Create new objects
            obj = self.species_objects[idx]
            new_color = self.fitness_to_color(new_fitness)
            
            # Animate sphere color change
            animations.append(
                obj['sphere'].animate.set_color(new_color)
            )
            
            # Animate bar height change
            new_height = new_fitness * self.BAR_MAX_HEIGHT
            new_bar = Cylinder(
                radius=self.SPHERE_RADIUS * 0.6,
                height=new_height,
                color=new_color,
                resolution=(8, 8)
            )
            new_bar.move_to([
                obj['bar'].get_center()[0],
                obj['bar'].get_center()[1],
                new_height / 2
            ])
            
            animations.append(Transform(obj['bar'], new_bar))
        
        # Play all replacement animations together
        self.play(*animations, run_time=0.4)
    
    def update_fitness_graph(self, bars, fitness_values):
        """Update the fitness distribution chart."""
        # Create new bars with updated colors and heights
        new_bars = BarChart(
            values=fitness_values,
            bar_names=[str(i) for i in range(self.NUM_SPECIES)],
            y_range=[0, 1, 0.2],
            x_length=4.5,
            y_length=2.3,
            bar_width=0.12,
            bar_colors=[self.fitness_to_color(f) for f in fitness_values]
        )
        # Use stored center if available, otherwise fallback
        if hasattr(self, 'graph_center'):
            new_bars.move_to(self.graph_center)
        else:
            new_bars.to_corner(DL, buff=1.0)
        
        # Transform to new chart
        self.play(Transform(bars, new_bars), run_time=0.3)
    
    def update_iteration_counter(self, iteration_label, iteration):
        """Update iteration display."""
        new_label = Text(
            f"Iteration: {iteration}", 
            font_size=24, 
            color=YELLOW
        )
        new_label.to_corner(UR)
        
        self.remove(iteration_label)
        self.add_fixed_in_frame_mobjects(new_label)
        self.add(new_label)
        
        # Update reference for next iteration
        return new_label
    
    def remove_highlights(self, neighbor_indices):
        """Remove avalanche highlighting effects."""
        if hasattr(self, 'highlight_rings'):
            self.play(FadeOut(self.highlight_rings), run_time=0.2)
    
    def finale(self):
        """Create concluding animation with mathematical summary."""
        # Stop camera rotation
        self.stop_ambient_camera_rotation()
        
        # Create summary text
        summary = VGroup(
            Text("Key Insights:", font_size=32, weight=BOLD, color=BLUE),
            Text("• Self-Organized Criticality emerges", font_size=28),
            Text("• Power Law distributions in avalanches", font_size=28),
            Text("• Punctuated Equilibrium dynamics", font_size=28),
            Text("• Universal behavior across scales", font_size=28),
            Text("Bak & Sneppen, Phys. Rev. Lett. 71, 4083 (1993)", 
                 font_size=20, color=GRAY)
        )
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        summary.to_corner(DL)
        
        # Add fixed positioning
        self.add_fixed_in_frame_mobjects(summary)
        
        # Animate in
        self.play(
            LaggedStart(
                *[Write(line) for line in summary],
                lag_ratio=0.1
            ),
            run_time=3
        )
        
        # Final dramatic rotation
        self.move_camera(phi=60 * DEGREES, theta=0 * DEGREES, zoom=0.6)
        self.wait(2)
        
        # Fade out
        self.play(FadeOut(summary))
        self.wait(1)


class BakSneppenHistogram(Scene):
    """
    Supplementary scene showing fitness distribution evolution.
    Demonstrates how the system approaches critical state.
    """
    
    def construct(self):
        # Title
        title = Text(
            "Fitness Distribution Evolution", 
            font_size=36, 
            weight=BOLD
        )
        title.to_edge(UP)
        self.add(title)
        
        # Initial histogram (random distribution)
        num_species = 100
        fitnesses = [random.random() for _ in range(num_species)]
        
        # Create axes
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, num_species/5, 5],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": False}
        )
        axes.shift(DOWN * 0.5)
        
        # Histogram
        hist = axes.plot_histogram(
            fitnesses,
            bins=20,
            color=BLUE,
            fill_opacity=0.7
        )
        
        # Labels
        x_label = Text("Fitness", font_size=24)
        y_label = Text("Count", font_size=24)
        x_label.next_to(axes, DOWN)
        y_label.next_to(axes, LEFT).rotate(PI/2)
        
        # Add elements
        self.add(axes, hist, x_label, y_label)
        
        # Simulate evolution
        for _ in range(30):
            # Find min and neighbors
            min_idx = fitnesses.index(min(fitnesses))
            neighbors = [
                (min_idx - 1) % num_species,
                min_idx,
                (min_idx + 1) % num_species
            ]
            
            # Replace
            for idx in neighbors:
                fitnesses[idx] = random.random()
            
            # Update histogram
            new_hist = axes.plot_histogram(
                fitnesses,
                bins=20,
                color=BLUE,
                fill_opacity=0.7
            )
            
            self.play(Transform(hist, new_hist), run_time=0.2)
        
        # Show critical state
        critical_text = Text(
            "Critical State Achieved", 
            font_size=28, 
            color=GREEN
        )
        critical_text.next_to(axes, UP)
        self.play(Write(critical_text))
        
        self.wait(2)


class BakSneppenAvalanche(ThreeDScene):
    """
    Close-up visualization of a single avalanche cascade.
    Shows the detailed mechanics of species replacement.
    """
    
    def construct(self):
        # Setup
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # Title
        title = Text(
            "Avalanche Cascade (Close-up)", 
            font_size=32,
            weight=BOLD
        )
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.add(title)
        
        # Create small system for clarity
        num_species = 12
        radius = 3
        
        species = []
        fitnesses = []
        
        for i in range(num_species):
            angle = 2 * np.pi * i / num_species
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = 0
            
            fitness = random.random()
            fitnesses.append(fitness)
            
            # Sphere
            sphere = Sphere(
                center=(x, y, z),
                radius=0.3,
                color=interpolate_color(RED, GREEN, fitness)
            )
            
            # Label
            label = Text(str(i), font_size=20, color=WHITE)
            label.move_to([x, y, -0.8])
            
            species.append(VGroup(sphere, label))
            self.add(sphere, label)
        
        # Show one avalanche in detail
        min_idx = fitnesses.index(min(fitnesses))
        neighbors = [
            (min_idx - 1) % num_species,
            min_idx,
            (min_idx + 1) % num_species
        ]
        
        # Highlight
        highlight = VGroup()
        for idx in neighbors:
            ring = Circle(radius=0.5, color=YELLOW, stroke_width=4)
            ring.move_to(species[idx][0].get_center())
            highlight.add(ring)
        
        self.play(Create(highlight))
        
        # Show replacement
        arrows = VGroup()
        for idx in neighbors:
            arrow = Arrow(
                start=UP * 2,
                end=species[idx][0].get_center(),
                color=RED,
                stroke_width=3
            )
            arrows.add(arrow)
        
        self.play(Create(arrows))
        
        # Animate replacements
        for idx in neighbors:
            new_fitness = random.random()
            new_color = interpolate_color(RED, GREEN, new_fitness)
            
            self.play(
                species[idx][0].animate.set_color(new_color),
                run_time=0.5
            )
        
        self.wait(1)
        self.play(FadeOut(highlight), FadeOut(arrows))
        self.wait(1)


# Production Configuration
# Render with: manim -pqh bak_sneppen_3d.py BakSneppenEvolution3D
# Or render all: manim -pqh bak_sneppen_3d.py

if __name__ == "__main__":
    # Optional: Direct execution for testing
    import subprocess
    
    scenes = [
        "BakSneppenEvolution3D",
        "BakSneppenHistogram", 
        "BakSneppenAvalanche"
    ]
    
    print("Bak-Sneppen Model Visualization")
    print("=" * 40)
    print("Available scenes:")
    for i, scene in enumerate(scenes, 1):
        print(f"{i}. {scene}")
    print("\nRender with:")
    print(f"manim -pqh bak_sneppen_3d.py {scenes[0]}")