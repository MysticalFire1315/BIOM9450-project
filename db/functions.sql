-----------------------
--***** GENERAL *****--
-----------------------
-- Raises permission denied error
CREATE OR REPLACE FUNCTION permission_denied ()
    RETURNS TRIGGER
    AS $$
BEGIN
    RAISE EXCEPTION 'Error: Permission Denied';
END;
$$
LANGUAGE plpgsql;

-----------
-- USER
-----------
-- Always use default `id` and `created_at` at insert
CREATE OR REPLACE FUNCTION default_users_function ()
    RETURNS TRIGGER
    AS $$
BEGIN
    NEW.id := DEFAULT;
    NEW.created_at := DEFAULT;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- Only allows updates to password_hash or person_id
CREATE OR REPLACE FUNCTION users_update_permission()
RETURNS TRIGGER AS $$
BEGIN
  -- Check if any column other than password_hash or person_id is being updated
  IF NOT (NEW.password_hash = OLD.password_hash OR NEW.person_id = OLD.person_id) THEN
    RAISE EXCEPTION 'Only password_hash and person_id can be updated';
  END IF;

  -- Allow the update if only allowed fields are changed
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


----------------------
-- BLACKLIST_TOKEN
----------------------
-- Always use default `blacklisted_on` at insert
CREATE OR REPLACE FUNCTION default_blacklist_tokens_function ()
    RETURNS TRIGGER
    AS $$
BEGIN
    NEW.blacklisted_on := DEFAULT;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

