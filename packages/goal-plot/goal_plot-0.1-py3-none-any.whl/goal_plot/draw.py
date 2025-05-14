import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_goal(ax, x=36, y=0, goal_width=8, goal_height=2.67,
                    net_lines=6, post_color='white', net_color='lightgray'):
    """
    Dessine un but 2D stylisé (vue de face) sur un axe matplotlib.

    Parameters:
    - ax : matplotlib axis
    - x, y : position du poteau gauche (en yards)
    - goal_width : largeur du but (yards)
    - goal_height : hauteur du but (yards)
    - net_lines : densité de lignes de filet
    - post_color : couleur des poteaux et barre transversale
    - net_color : couleur des lignes du filet
    """

    # Fond noir pour l'axe
    ax.set_facecolor('black')

    # Poteaux (2 verticaux)
    post_width = 0.15
    left_post = patches.Rectangle((x, y), post_width, goal_height, 
                                  color=post_color, zorder=3, ec='black', lw=1.5)
    right_post = patches.Rectangle((x + goal_width - post_width, y), 
                                   post_width, goal_height, color=post_color, zorder=3, ec='black', lw=1.5)

    # Barre transversale (horizontal)
    crossbar = patches.Rectangle((x, y + goal_height - post_width), 
                                 goal_width, post_width, color=post_color, zorder=3, ec='black', lw=1.5)

    # Ajouter poteaux et barre
    ax.add_patch(left_post)
    ax.add_patch(right_post)
    ax.add_patch(crossbar)

    # Filet - lignes verticales
    x_lines = np.linspace(x + post_width, x + goal_width - post_width, net_lines)
    for xi in x_lines:
        ax.plot([xi, xi], [y, y + goal_height - post_width], 
                color=net_color, linewidth=0.6, zorder=1)

    # Filet - lignes horizontales
    y_lines = np.linspace(y, y + goal_height - post_width, net_lines)
    for yi in y_lines:
        ax.plot([x + post_width, x + goal_width - post_width], [yi, yi], 
                color=net_color, linewidth=0.6, zorder=1)

    # Sol devant le but (facultatif, effet visuel)
    ground_strip = patches.Rectangle((x, y - 0.15), goal_width, 0.15, 
                                     facecolor='gray', edgecolor='none', alpha=0.25, zorder=0)
    ax.add_patch(ground_strip)

    # Optionnel : ajuster la vue avec marge pour tirs off target
    ax.set_xlim(x - 2, x + goal_width + 2)
    ax.set_ylim(y - 0.5, y + goal_height + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')