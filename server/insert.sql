-- Sample entries for the users table
INSERT INTO users (master_user, master_password) VALUES
('user1', 'password1'),
('user2', 'password2'),
('user3', 'password3');

-- Sample entries for the passwords table
INSERT INTO passwords (id_user, s_url_path, s_username, s_password) VALUES
(1, 'https://example.com', 'user1@example.com', 'user1_password'),
(1, 'https://example.org', 'user1_org', 'org_password1'),
(2, 'https://test.com', 'test_user', 'test_password'),
(3, 'https://example.net', 'user3_net', 'net_password3');
