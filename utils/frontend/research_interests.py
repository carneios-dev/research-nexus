# Utility function for the word cloud widget that allows for random color selection from a list of colors.
def random_color(word, font_size, position, orientation, random_state=None, **kwargs):
    from random import choice
    colors = ['#333', '#FF5F05', '#001630', '#F0884D', '#014DA3']
    return choice(colors)
