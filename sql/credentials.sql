SELECT username, password
FROM `{{ project }}.{{ dataset }}.users`
WHERE username = '{{ username }}'