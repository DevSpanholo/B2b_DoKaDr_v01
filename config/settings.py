"""
Configuration settings for the bot
"""

DELAYS = {
    'position': 1.0,  # Delay when configuring positions
    'gather': 2.0,    # Delay after gathering resource
    'mapChange': 0.5  # Delay between map changes
}

SCREEN = {
    'darkThreshold': 50  # Threshold for detecting dark screen during map change
}

RESOURCE_CONFIDENCE = 0.8  # Confidence level for resource image detection