from viktor import ViktorController


class Controller(ViktorController):
    label = 'My Folder'
    children = ['MyEntityType']
    show_children_as = 'Table'  # or 'Cards'
