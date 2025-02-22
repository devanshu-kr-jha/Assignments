DO $$ 
BEGIN 
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test') THEN 
      CREATE DATABASE test; 
   END IF; 
END $$;
