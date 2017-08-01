import json

# Get resources as a python dictionary
resource_text_file = open("atlas-new-format-resources-export.json")
resources = json.loads(resource_text_file.read())


resource_table = {}

count = 0
for key in resources:
	# key corresponds to the entity that uploaded the file.
	entity_resources = resources[key]
	for k in entity_resources:
		# k corresponds to the resource itself.
		resource = entity_resources[k]
		# Fields required should be name, type (called category), topic, upload date
		# Remove filetype
		resource.pop('filetype', None)
		# Add topic globally
		resource['topic'] = ''
		# Additional fields are entity_uploader, which tracks who uploaded the resource, and
		#	downloadURL, which locates the resource in firebase.
		resource['entity_uploader'] = key
		# Add the resource to the resource table
		resource_table[k] = resource

# Resource table is now made of key:value pairs.
#	key: unique resource key
#	value: object that contains--
#		name 			:	resource name
#		category		:	resource type
#		topic			:	main topic (can this be multiple?)
#		upload_date		:	date resource was uploaded
#		downloadURL		:	location resource was uploaded to in Firebase, where users can see the file or it can be downloaded from
#		entity_uploader :	the key of the entity that uploaded this file.


# Write the result
target_file = open("atlas-resource-table.json", "w")
target_file.write(json.dumps(resource_table))
target_file.close()