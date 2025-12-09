"""Content Planning Panel for SonicSleep Pro.

This panel provides content planning and scheduling features:
- Generate content plans for multiple videos
- Schedule optimal upload times
- Track content calendar
"""

import csv
import json
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

logger = logging.getLogger(__name__)


class ContentPlanningPanel:
    """Panel for content planning and scheduling."""

    def __init__(self, panel):
        self.panel = panel
        self.content_frame = panel.content_frame

        # Initialize orchestrator (lazy load)
        self._orchestrator = None

        # Current content plan
        self.current_plan = []

        # Create the main UI
        self._create_ui()

    @property
    def orchestrator(self):
        """Lazy-load the orchestrator."""
        if self._orchestrator is None:
            from project_name.core.orchestrator import AutotubeOrchestrator

            self._orchestrator = AutotubeOrchestrator()
        return self._orchestrator

    def _create_ui(self):
        """Create the user interface."""
        # Title
        ttk.Label(
            self.content_frame,
            text="Content Planning & Scheduling",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        # Controls frame
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)

        # Number of videos
        ttk.Label(controls_frame, text="Number of Videos:").pack(side=tk.LEFT, padx=5)
        self.num_videos_var = tk.StringVar(value="7")
        ttk.Spinbox(
            controls_frame,
            from_=1,
            to=30,
            textvariable=self.num_videos_var,
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        # Generate button
        ttk.Button(
            controls_frame,
            text="📅 Generate Content Plan",
            command=self._generate_plan,
        ).pack(side=tk.LEFT, padx=10)

        # Export button
        ttk.Button(
            controls_frame, text="💾 Export Plan", command=self._export_plan
        ).pack(side=tk.LEFT, padx=5)

        # Plan display frame
        plan_frame = ttk.LabelFrame(
            self.content_frame, text="Content Plan", padding="10"
        )
        plan_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create treeview for plan display
        columns = (
            "video_number",
            "sound_type",
            "purpose",
            "scheduled_date",
            "optimal_time",
            "duration",
        )
        self.plan_tree = ttk.Treeview(
            plan_frame, columns=columns, show="headings", height=15
        )

        # Define headings
        self.plan_tree.heading("video_number", text="#")
        self.plan_tree.heading("sound_type", text="Sound Type")
        self.plan_tree.heading("purpose", text="Purpose")
        self.plan_tree.heading("scheduled_date", text="Date")
        self.plan_tree.heading("optimal_time", text="Time")
        self.plan_tree.heading("duration", text="Duration")

        # Define column widths
        self.plan_tree.column("video_number", width=40)
        self.plan_tree.column("sound_type", width=120)
        self.plan_tree.column("purpose", width=80)
        self.plan_tree.column("scheduled_date", width=100)
        self.plan_tree.column("optimal_time", width=80)
        self.plan_tree.column("duration", width=80)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            plan_frame, orient=tk.VERTICAL, command=self.plan_tree.yview
        )
        self.plan_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.plan_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Statistics frame
        stats_frame = ttk.LabelFrame(
            self.content_frame, text="Plan Statistics", padding="10"
        )
        stats_frame.pack(fill=tk.X, padx=10, pady=10)

        self.stats_text = tk.StringVar(value="No plan generated yet")
        ttk.Label(stats_frame, textvariable=self.stats_text).pack()

    def _generate_plan(self):
        """Generate a content plan."""
        try:
            num_videos = int(self.num_videos_var.get())
            if num_videos <= 0:
                raise ValueError("Number of videos must be positive")

            # Clear existing plan
            for item in self.plan_tree.get_children():
                self.plan_tree.delete(item)

            # Generate plan
            self.current_plan = self.orchestrator.plan_content(num_videos=num_videos)

            # Display plan
            for item in self.current_plan:
                self.plan_tree.insert(
                    "",
                    tk.END,
                    values=(
                        item["video_number"],
                        item["sound_type"],
                        item["purpose"],
                        item["scheduled_date"],
                        item["optimal_time"],
                        f"{item['duration_hours']}h",
                    ),
                )

            # Update statistics
            self._update_statistics()

            messagebox.showinfo(
                "Success", f"Generated plan for {num_videos} videos!"
            )

        except Exception as e:
            logger.error(f"Error generating plan: {e}")
            messagebox.showerror("Error", f"Failed to generate plan: {e}")

    def _export_plan(self):
        """Export the content plan to a file."""
        if not self.current_plan:
            messagebox.showwarning("No Plan", "Generate a plan first before exporting")
            return

        # Ask user for file format
        file_path = filedialog.asksaveasfilename(
            title="Export Content Plan",
            defaultextension=".json",
            filetypes=[
                ("JSON Files", "*.json"),
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ],
        )

        if not file_path:
            return

        try:
            if file_path.endswith(".json"):
                with open(file_path, "w") as f:
                    json.dump(self.current_plan, f, indent=2)
            elif file_path.endswith(".csv"):
                # Redundant check removed - already verified on line 175
                with open(file_path, "w", newline="") as f:
                        writer = csv.DictWriter(f, fieldnames=self.current_plan[0].keys())
                        writer.writeheader()
                        writer.writerows(self.current_plan)
            else:
                # Text format
                with open(file_path, "w") as f:
                    f.write("Content Plan\n")
                    f.write("=" * 70 + "\n")
                    f.write(
                        f"{'#':<3} {'Sound Type':<15} {'Purpose':<10} {'Date':<12} "
                        f"{'Time':<8} {'Duration':<8}\n"
                    )
                    f.write("-" * 70 + "\n")
                    for item in self.current_plan:
                        f.write(
                            f"{item['video_number']:<3} {item['sound_type']:<15} "
                            f"{item['purpose']:<10} {item['scheduled_date']:<12} "
                            f"{item['optimal_time']:<8} {item['duration_hours']}h\n"
                        )
                    f.write("=" * 70 + "\n")

            messagebox.showinfo("Success", f"Content plan exported to: {file_path}")

        except Exception as e:
            logger.error(f"Error exporting plan: {e}")
            messagebox.showerror("Error", f"Failed to export plan: {e}")

    def _update_statistics(self):
        """Update plan statistics."""
        if not self.current_plan:
            self.stats_text.set("No plan generated yet")
            return

        # Calculate statistics
        total_videos = len(self.current_plan)
        sound_types = {}
        purposes = {}
        total_hours = 0

        for item in self.current_plan:
            sound_type = item["sound_type"]
            purpose = item["purpose"]
            duration = item["duration_hours"]

            sound_types[sound_type] = sound_types.get(sound_type, 0) + 1
            purposes[purpose] = purposes.get(purpose, 0) + 1
            total_hours += duration

        # Format statistics
        stats = f"Total Videos: {total_videos} | Total Duration: {total_hours}h | "
        stats += "Sound Types: " + ", ".join(
            [f"{k} ({v})" for k, v in sound_types.items()]
        )
        stats += " | Purposes: " + ", ".join(
            [f"{k} ({v})" for k, v in purposes.items()]
        )

        self.stats_text.set(stats)
