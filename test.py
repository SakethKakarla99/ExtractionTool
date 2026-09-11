from authorization_extractor import extract_authorization_form

member, provider = extract_authorization_form("documents/authorization_form.pdf")

print("\n--- MEMBER ---")
print(member)

print("\n--- Provider ---")
print(provider)
