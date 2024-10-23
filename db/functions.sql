-- Enforce defaults for `id` and `created_at` columns
CREATE OR REPLACE FUNCTION enforce_defaults_for_id_and_created_at ()
  RETURNS TRIGGER
  AS $$
BEGIN
  -- Ensure "id" and "created_at" are always defaulted during INSERT
  IF TG_OP = 'INSERT' THEN
    NEW.id := DEFAULT;
    NEW.created_at := DEFAULT;
  END IF;
  -- Prevent "id" modification during an UPDATE
  IF TG_OP = 'UPDATE' AND NEW.id IS DISTINCT FROM OLD.id THEN
    RAISE EXCEPTION 'Modifying "id" is not allowed';
  END IF;
  -- Prevent "created_at" modification during an UPDATE
  IF TG_OP = 'UPDATE' AND NEW.created_at IS DISTINCT FROM OLD.created_at THEN
    RAISE EXCEPTION 'Modifying "created_at" is not allowed';
  END IF;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;


-- Always use default `blacklisted_on` at insert
CREATE OR REPLACE FUNCTION default_blacklisted_on ()
  RETURNS TRIGGER
  AS $$
BEGIN
  NEW.blacklisted_on := DEFAULT;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- Raises permission denied error
CREATE OR REPLACE FUNCTION permission_denied()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Error: Permission Denied'
END;
$$ LANGUAGE plpgsql;