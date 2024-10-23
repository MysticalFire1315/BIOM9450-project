-- Cannot insert or update `id` or `created_at` columns
CREATE TRIGGER enforce_defaults_on_users
  BEFORE INSERT OR UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION enforce_defaults_for_id_and_created_at ();

-- Always use default `blacklisted_on` at insert
CREATE TRIGGER enforce_defaults_on_users
  BEFORE INSERT ON blacklist_tokens
  FOR EACH ROW
  EXECUTE FUNCTION default_blacklisted_on ();


-- Cannot update or delete from table `blacklist_tokens`
CREATE TRIGGER prevent_update_delete_trigger
BEFORE UPDATE OR DELETE ON blacklist_tokens
FOR EACH ROW
EXECUTE FUNCTION prevent_update_and_delete();