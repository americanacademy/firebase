import json

# Get entities data as a python dictionary
entity_text_file = open("atlas-769c1-entity-export.json")
entities = json.loads(entity_text_file.read())


# Parse through the entities
for key in entities:
	entity = entities[key]
	# Remove fields
	entity.pop('has_resources', None)
	entity.pop('has_linked_records', None)

# Write to the file
target_file = open("atlas-entity-table.json", "w")
target_file.write(json.dumps(entities))
target_file.close()
	