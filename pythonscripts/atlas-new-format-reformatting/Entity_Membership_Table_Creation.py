import json

# Get collaborations and organizations as python dictionaries
collab_text_file = open("atlas-new-format-collaborations-export.json")
collaborations = json.loads(collab_text_file.read())

org_text_file = open("atlas-new-format-organizations-export.json")
organizations = json.loads(org_text_file.read())

# Get a dictionary of collaboration key to empty arrays
membership_table = {key : [] for key in collaborations}

# Fill the arrays with the keys of the collaboration members

def get_keys(mem_str):
	"""Gets all the keys in an array from a 'collaboration_links' style string."""
	items_list = []
	if mem_str: 
		items_list = mem_str.split('||')
	tag_list = [item.split('|')[1].strip() for item in items_list]
	return tag_list
# key_list lists organization keys and then the collaborations they are linked to
key_list = {}
current_org = {}
for key in organizations:
	org = organizations[key]
	current_org = org
	key_list[key] = get_keys(org['collaboration_links'])

for key in collaborations:
	collab = collaborations[key]
	org_link = collab.pop('organization_links', '')
	if org_link:
		membership_table[key] = get_keys(org_link)

for key in key_list:
	for k in key_list[key]:
		membership_table[k].append(key)

target_file = open("atlas-entity-membership-table.json", "w")
target_file.write(json.dumps(membership_table))
target_file.close()
