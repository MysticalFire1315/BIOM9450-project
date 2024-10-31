-----------
-- USERS
-----------
-- Use defaults on insert
DROP TRIGGER IF EXISTS default_users_trigger ON users;
CREATE TRIGGER default_users_trigger
    BEFORE INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION default_users_function ();

-- Restrict updates to specific fields
DROP TRIGGER IF EXISTS users_update_permission_trigger ON users;
CREATE TRIGGER users_update_permission_trigger
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION users_update_permission();

-- Set permissions to deny delete
DROP TRIGGER IF EXISTS users_permissions ON users;
CREATE TRIGGER users_permissions
    BEFORE DELETE ON users
    FOR EACH ROW
    EXECUTE FUNCTION permission_denied ();

----------------------
-- BLACKLIST_TOKENS
----------------------
-- Use defaults on insert
DROP TRIGGER IF EXISTS default_blacklist_tokens_trigger ON blacklist_tokens;
CREATE TRIGGER default_blacklist_tokens_trigger
    BEFORE INSERT ON blacklist_tokens
    FOR EACH ROW
    EXECUTE FUNCTION default_blacklist_tokens_function ();

-- Set permissions to deny update or delete
DROP TRIGGER IF EXISTS blacklist_tokens_permissions ON blacklist_tokens;
CREATE TRIGGER blacklist_tokens_permissions
    BEFORE UPDATE OR DELETE ON blacklist_tokens
    FOR EACH ROW
    EXECUTE FUNCTION permission_denied ();

