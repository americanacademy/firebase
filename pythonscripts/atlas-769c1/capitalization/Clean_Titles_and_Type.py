# This file does the following:
#	- Make lowercase the words in 'word_replacements' that are not at the start of entity names
#	- Make the entity category 'Ngo' to 'NGO'
#	- Make the entity category field for NGOs by merging the entity_category_info
#	- Remove extra fields and push corresponding backend updates


import json

# Get entities data as a python dictionary
entity_text_file = open("atlas-769c1-entity-export.json")
entities = json.loads(entity_text_file.read())

for key in entities:
	entity = entities[key]

	name = entity['entity_name']
	# Store the first letter and remove it from the working part.
	# This is so the first word of the title is not a complete word.
	first_letter = name[0]
	trunc_name = name[1:]
	# Lowercase list of words to replace.
	word_replacements = ['a ', 'an ', 'and ', 'at ', 'but ', 'by ', 'for ', 'in ', 'of ', 'on ', 'or ', 'out ', 'so ', 'the ', 'to ']

	# Replace each word in word_replacements that's capitalized with its lowercase equivalent
	for word in word_replacements:
		upper_word = word[0].upper() + word[1:]
		trunc_name = trunc_name.replace(upper_word, word)


	# print(first_letter + trunc_name)
	entity['entity_name'] = first_letter + trunc_name

	# Rename "Ngo" to "NGO"
	entity_category = entity['entity_category']
	if entity_category == "Ngo":
		entity['entity_category'] = "NGO"

	# Remove whitespace
	entity['entity_category_info'] = entity['entity_category_info'].strip()


	if entity['entity_category'] == "NGO":
		if entity['entity_category_info']:
			entity['entity_category'] = "NGO - " + entity['entity_category_info']
		else:
			entity['entity_category'] = "NGO - other"

	if entity['entity_category'] == "" and entity['entity_category_info']:
		entity['entity_category'] = "NGO - " + entity['entity_category_info']


	# Remove extra fields
	entity.pop('has_resources', None)
	entity.pop('has_linked_records', None)
	entity.pop('organization_links', None)
	entity.pop('participation_membership_in_collaboration', None)
	entity.pop('entity_category_info')


# Write to the file
target_file = open("atlas-entity-table.json", "w")
target_file.write(json.dumps(entities))
target_file.close()