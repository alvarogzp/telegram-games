def formatted_user(user):
    if user.username is not None:
        formatted = "@" + user.username
    elif user.first_name is not None:
        formatted = user.first_name
        if user.last_name is not None:
            formatted += " " + user.last_name
    else:
        formatted = str(user.id)
    return formatted
