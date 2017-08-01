## 
## 
## Takes all records from atlas-new-format table and converts organizations and
## 	collaborations to a unified "entity" type data structure
## Requires being in same directory as organization and collaboration json
## 	dumps. Requires json python module.
##
## Final entity attributes
##	-entity name
##	-entity type
##	-about
##	-status (previously active)
## 	-primary focus (previously issues)
##	-contact
##	-address 1
##	-city
##	-state
## 	-zip
##	-entity category (previously collaboration type)
##	-entity category info
##	-facebook
## 	-has linked records
## 	-twitter
##	-updated date
##	-linkedin company page
##	-linkedin company groups
##	-youtube
##	-website
## Organization specific attributes
##	-fortune status
##	-geolocation
##	-Washington DC office
## Collaboration specific attributes
## 	-abbreviation
##	-collaboration membership verified by
##	-founding year
##	-address dc office
##	-has resources
## Legacy fields to be removed
##  -organization links
##	-participation membership in collaboration
##
##

import json

# Get collaborations and organizations as python dictionaries
collab_text_file = open("atlas-new-format-collaborations-export.json")
collaborations = json.loads(collab_text_file.read())

org_text_file = open("atlas-new-format-organizations-export.json")
organizations = json.loads(org_text_file.read())

# Fix collaborations as python dictionary
for key in collaborations:
	# Collab is the single collaboration being edited
	collab = collaborations[key]

	collab['entity_type'] = 'collaboration'
	
	# Remove fields
	collab.pop('LetterregardingtheHONESTAct', None)
	collab.pop("letterregardingthehonestact", None)

	collab.pop('collaboration_links', None)

	collab.pop('file_type', None)

	collab.pop('file type', None)
		
	# participation_membership_in_collaboration is a legacy field and
	#	should be removed as soon as confident
	#collab.pop('participation_membership_in_collaboration')

	collab.pop('link_to_folder_sites')
	
	collab.pop('membership_fees')

	collab.pop('status')

	collab.pop('category', None)

	collab.pop('organization_category')
	# Fill in the gaps where some records don't have the field
	collab['has_resources'] = collab.pop('has_resources', False)

	has_linked_records = collab.pop('has_linked_records', 'false')

	if has_linked_records == 'true':
		collab['has_linked_records'] = True
	else:
		collab['has_linked_records'] = False

	# organization_links is a field that should be managed by external scripts
	# I'm keeping it in for legacy but it should be removed when possible
	# TODO: See where this is actually used and phase it out.
	collab['organization_links'] = collab.pop('organization_links', '')
	
	# Rename field names
	collab['status'] = collab.pop('active')

	collab['primary_focus'] = collab.pop('issues')

	collab['entity_name'] = collab.pop('organization_name')

	collab['entity_category_info'] = collab.pop('collaboration_type_info')
	# Tricky work with collaboration types: currently stored in two zones
	# Rename to entity_category
	collab_type = collab.pop('collaboration_type')
	type_collab = collab.pop('type_of_collaboration')

	if collab_type and not type_collab:
		collab['entity_category'] = collab_type
	elif not collab_type and type_collab:
		collab['entity_category'] = type_collab
	# This is a one error handling case
	elif collab_type and type_collab and collab_type != type_collab:
		collab['entity_category'] = 'Letter/Statement'
	else:
		collab['entity_category'] = type_collab

	# Add shared fields
	collab['washington_dc_office'] = ''

	collab['fortune_status'] = ''

for key in organizations:
	org = organizations[key]

	org['entity_type'] = 'organization'
	# Remove fields
	# As above, participation_membership_in_collaboration is a legacy field
	#	and should be removed as soon as possible.
	#org.pop('participation_membership_in_collaboration')

	org.pop('collaboration_links')

	org.pop('__firebaseKey__', None)

	org.pop('organization_type_info')

	org.pop('file type', None)

	org.pop('category', None)

	# Modify field contents 
	org['address_1'] += org.pop('address_2')

	org['has_linked_records'] = org.pop('has_linked_records', False)

	# Rename fields
	org['fortune_status'] = org.pop('2015_fortune_1000_50010010')

	org['entity_name'] = org.pop('organization_name')

	org['primary_focus'] = org.pop('scope_focus')

	org['contact'] = org.pop('government_relations_contact_person')

	org['washington_dc_office'] = org.pop('address_1_dc_office')

	org['entity_category'] = org.pop('organization_category')

	org['entity_category_info'] = org.pop('nonprofit_status')

	# Add shared fields
	org['status'] = ''

	org['geolocation'] = org.pop('geolocation', '')

	org['has_resources'] = False

	org['founding_year_for_collaborations_only'] = ''

	org['collaboration_participation_membership_verified_by'] = ''

	org['abbreviations_for_collaborations_only'] = ''
	# Redundant field, phase this out with organization links from above
	org['organization_links'] = ''

# Merge two types of entity entries
entities = collaborations.copy()
entities.update(organizations)

# Write the output
"""
target_file = open("atlas-entity-table.json", "w")
target_file.write(json.dumps(entities))
target_file.close()

"""