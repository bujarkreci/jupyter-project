 CREATE OR REPLACE FUNCTION export_testings(file_name VARCHAR(255)) RETURNS void 
  AS $$
  DECLARE
    select_stmt VARCHAR(100) := 'SELECT c.id, c.name FROM testing c';
  BEGIN
     EXECUTE('\copy (' || select_stmt || ') to ' || QUOTE_LITERAL(file_name) || ' with csv'); 
  END;
  $$
  LANGUAGE plpgsql;
  
    -- Execute function to export data to CSV file 
  SELECT export_testings(E'C:\\Users\\NoteBook\\postgreconnExample\\data\\testings.csv');