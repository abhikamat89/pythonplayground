import streamlit as st
import pandas as pd

# Example DataFrame
data = {
    'Level': [1, 2, 2, 3, 3],
    'Parent': [None, 1, 1, 2, 2],
    'Item': ['Level 1 Item', 'Level 2 Item 1', 'Level 2 Item 2', 'Level 3 Item 1', 'Level 3 Item 2']
}
df = pd.DataFrame(data)

def build_tree(df, parent=None, level=1):
    tree = []
    for _, row in df[df['Parent'] == parent].iterrows():
        subtree = {
            'item': row['Item'],
            'children': build_tree(df, row['Level'], level + 1)
        }
        tree.append(subtree)
    return tree

def render_tree(level, tree):
    indent = "&nbsp;" * (level * 4)  # HTML non-breaking space for indentation
    for node in tree:
        if node['children']:
            if st.checkbox(f"{' ' * (level * 2)}{node['item']}", key=f"level_{level}_{node['item']}"):
                render_tree(level + 1, node['children'])
        else:
            st.markdown(f"{indent}{node['item']}", unsafe_allow_html=True)

st.title('Collapsible Tree Structure from DataFrame')

# Build the tree structure from DataFrame
tree_data = build_tree(df)

# Render the tree
render_tree(1, tree_data)