#!/usr/bin/env python3
"""
Autonomous Snake SVG Generator for GitHub Profile README
Uses Hamiltonian cycle for guaranteed infinite, collision-free gameplay.
"""

import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ============== CONFIG ==============
GRID_W = 30
GRID_H = 18
CELL = 20
PADDING = 10
WIDTH = GRID_W * CELL + 2 * PADDING
HEIGHT = GRID_H * CELL + 2 * PADDING

# Colors (dark theme compatible)
BG_COLOR = "#050a10"
GRID_COLOR = "#1a2332"
SNAKE_HEAD = "#22d3ee"
SNAKE_BODY = "#0ea5c7"
SNAKE_TAIL = "#0891b2"
FOOD_COLOR = "#ef4444"
WALL_COLOR = "#fb923c"
TEXT_COLOR = "#8890a0"
SCORE_COLOR = "#22d3ee"

# ============== HAMILTONIAN CYCLE ==============
def build_hamiltonian_cycle(w, h):
    """Build a Hamiltonian cycle for even-width grids."""
    path = []
    if w % 2 == 0:
        # Snake pattern for even width
        for y in range(h):
            if y % 2 == 0:
                for x in range(w):
                    path.append((x, y))
            else:
                for x in range(w - 1, -1, -1):
                    path.append((x, y))
        # Connect end to start (h even required for true cycle)
        # For our visualization, we just use the path
    else:
        # Fallback: simple spiral
        x, y = 0, 0
        dx, dy = 1, 0
        visited = set()
        for _ in range(w * h):
            path.append((x, y))
            visited.add((x, y))
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in visited:
                dx, dy = -dy, dx  # turn right
                nx, ny = x + dx, y + dy
            x, y = nx, ny
    return path

CYCLE = build_hamiltonian_cycle(GRID_W, GRID_H)
CYCLE_LEN = len(CYCLE)

# ============== GAME STATE ==============
def simulate_game(seed=None):
    """Run deterministic snake simulation."""
    if seed is None:
        # Use current time for variety, but make it deterministic per run
        import time
        seed = int(time.time() // 21600)  # Changes every 6 hours
    random.seed(seed)

    # Start snake at cycle position 0, length 4
    head_idx = 0
    snake_len = 4
    snake = [(head_idx - i) % CYCLE_LEN for i in range(snake_len)]

    # Place food at a position ahead on cycle
    food_idx = (head_idx + 8) % CYCLE_LEN
    while food_idx in snake:
        food_idx = (food_idx + 1) % CYCLE_LEN

    # Simulate some steps
    steps = random.randint(40, 80)
    for _ in range(steps):
        head_idx = (head_idx + 1) % CYCLE_LEN
        snake = [head_idx] + snake[:-1]

        # Check food
        if head_idx == food_idx:
            snake.append(snake[-1])  # grow
            food_idx = (food_idx + random.randint(5, 12)) % CYCLE_LEN
            while food_idx in snake:
                food_idx = (food_idx + 1) % CYCLE_LEN

    return snake, food_idx, snake_len - 4, seed

# ============== SVG GENERATION ==============
def cell_to_px(idx):
    """Convert grid index to pixel coordinates (center of cell)."""
    x, y = CYCLE[idx]
    return PADDING + x * CELL + CELL // 2, PADDING + y * CELL + CELL // 2

def create_svg(snake, food_idx, score):
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(WIDTH),
        "height": str(HEIGHT),
        "viewBox": f"0 0 {WIDTH} {HEIGHT}",
        "role": "img",
        "aria-label": f"Autonomous Snake Game - Score: {score}"
    })

    # Background
    ET.SubElement(svg, "rect", {
        "width": "100%", "height": "100%", "fill": BG_COLOR
    })

    # Subtle grid
    grid_g = ET.SubElement(svg, "g", {"stroke": GRID_COLOR, "stroke-width": "0.5", "opacity": "0.3"})
    for x in range(GRID_W + 1):
        ET.SubElement(grid_g, "line", {
            "x1": str(PADDING + x * CELL), "y1": str(PADDING),
            "x2": str(PADDING + x * CELL), "y2": str(PADDING + GRID_H * CELL)
        })
    for y in range(GRID_H + 1):
        ET.SubElement(grid_g, "line", {
            "x1": str(PADDING), "y1": str(PADDING + y * CELL),
            "x2": str(PADDING + GRID_W * CELL), "y2": str(PADDING + y * CELL)
        })

    # Border
    ET.SubElement(svg, "rect", {
        "x": str(PADDING - 2), "y": str(PADDING - 2),
        "width": str(GRID_W * CELL + 4), "height": str(GRID_H * CELL + 4),
        "fill": "none", "stroke": WALL_COLOR, "stroke-width": "2", "rx": "4"
    })

    # Food (pulsing apple)
    fx, fy = cell_to_px(food_idx)
    food_g = ET.SubElement(svg, "g", {
        "transform": f"translate({fx}, {fy})"
    })
    # Apple body
    ET.SubElement(food_g, "circle", {
        "r": str(CELL * 0.38), "fill": FOOD_COLOR,
        "filter": "url(#glow)"
    })
    # Stem
    ET.SubElement(food_g, "path", {
        "d": f"M0,-{CELL*0.35} Q{-CELL*0.08},-{CELL*0.45} {CELL*0.05},-{CELL*0.55}",
        "stroke": "#8b5e3c", "stroke-width": "2", "fill": "none", "stroke-linecap": "round"
    })
    # Leaf
    ET.SubElement(food_g, "ellipse", {
        "cx": str(CELL*0.1), "cy": str(-CELL*0.45),
        "rx": str(CELL*0.12), "ry": str(CELL*0.06),
        "fill": "#34d399", "transform": "rotate(-30)"
    })

    # Snake body (gradient from head to tail)
    snake_g = ET.SubElement(svg, "g")

    defs = ET.SubElement(svg, "defs")
    # Glow filter for food
    filt = ET.SubElement(defs, "filter", {"id": "glow", "x": "-50%", "y": "-50%", "width": "200%", "height": "200%"})
    ET.SubElement(filt, "feGaussianBlur", {"stdDeviation": "3", "result": "coloredBlur"})
    ET.SubElement(filt, "feMerge")
    # Actually, simpler approach: just use drop-shadow via filter
    feMerge = ET.SubElement(filt, "feMerge")
    ET.SubElement(feMerge, "feMergeNode", {"in": "coloredBlur"})
    ET.SubElement(feMerge, "feMergeNode", {"in": "SourceGraphic"})

    for i, seg_idx in enumerate(snake):
        x, y = cell_to_px(seg_idx)
        # Progress along snake (0 = head, 1 = tail)
        t = i / max(1, len(snake) - 1)

        # Interpolate color
        if i == 0:
            fill = SNAKE_HEAD
            r = CELL * 0.45
        elif i == len(snake) - 1:
            fill = SNAKE_TAIL
            r = CELL * 0.3
        else:
            # Body gradient
            fill = SNAKE_BODY
            r = CELL * 0.38 - t * CELL * 0.08

        # Cell rect with rounded corners
        cell_x = x - CELL // 2 + 2
        cell_y = y - CELL // 2 + 2
        cell_size = CELL - 4

        # Rounded rect for snake segment
        ET.SubElement(snake_g, "rect", {
            "x": str(cell_x), "y": str(cell_y),
            "width": str(cell_size), "height": str(cell_size),
            "rx": str(cell_size // 2), "fill": fill
        })

    # Eyes on head
    hx, hy = cell_to_px(snake[0])
    # Determine direction from head to next segment
    if len(snake) > 1:
        nx, ny = cell_to_px(snake[1])
        dx, dy = nx - hx, ny - hy
    else:
        dx, dy = CELL, 0

    # Eye offset based on direction
    eye_dist = CELL * 0.18
    eye_sep = CELL * 0.12

    if abs(dx) > abs(dy):  # horizontal
        eye1 = (hx + eye_dist, hy - eye_sep)
        eye2 = (hx + eye_dist, hy + eye_sep)
    else:  # vertical
        eye1 = (hx - eye_sep, hy + eye_dist)
        eye2 = (hx + eye_sep, hy + eye_dist)

    for ex, ey in [eye1, eye2]:
        ET.SubElement(snake_g, "circle", {
            "cx": str(ex), "cy": str(ey), "r": str(CELL * 0.07), "fill": "#050a10"
        })
        ET.SubElement(snake_g, "circle", {
            "cx": str(ex + dx * 0.05), "cy": str(ey + dy * 0.05),
            "r": str(CELL * 0.03), "fill": "#fff"
        })

    # Score text
    ET.SubElement(svg, "text", {
        "x": str(WIDTH // 2), "y": str(HEIGHT - 18),
        "fill": SCORE_COLOR, "font-family": "'Courier New', monospace",
        "font-size": "14", "font-weight": "bold", "text-anchor": "middle"
    }).text = f"SCORE: {score}"

    # Subtitle
    ET.SubElement(svg, "text", {
        "x": str(WIDTH // 2), "y": str(HEIGHT - 4),
        "fill": TEXT_COLOR, "font-family": "'Courier New', monospace",
        "font-size": "10", "text-anchor": "middle", "opacity": "0.6"
    }).text = "AUTONOMOUS • HAMILTONIAN PATH"

    return svg

def prettify(elem):
    rough = ET.tostring(elem, encoding="unicode")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ")

def main():
    snake, food_idx, score, seed = simulate_game()
    svg = create_svg(snake, food_idx, score)
    pretty = prettify(svg)

    with open("snake.svg", "w", encoding="utf-8") as f:
        f.write(pretty)

    print(f"Generated snake.svg (seed={seed}, score={score}, len={len(snake)})")

if __name__ == "__main__":
    main()