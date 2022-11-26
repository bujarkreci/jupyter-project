CREATE TABLE dbo.test123(
id INT NOT NULL
)

CREATE TYPE [dbo].[dboListInt] AS TABLE
(
    [Id] INT NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE or alter PROCEDURE dbo.testProc123 (@tvp [dbo].dboListInt READONLY)
AS
BEGIN
    SET NOCOUNT ON;
	insert into dbo.test123 (id)
    SELECT * FROM @tvp;

	SELECT t.id
	FROM dbo.test123 t;

END