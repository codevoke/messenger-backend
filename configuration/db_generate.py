General = '''
create table General(
    id integer primary key autoincrement,
    tag_id varchar(20) unique,
    email text,
    password varchar(20),
    firstname varchar(15),
    lastname varchar(15)
);

create trigger test after insert
    on General
    begin
        UPDATE General SET tag_id = ('id' || id) where id = (SELECT id FROM General ORDER BY id DESC LIMIT 1);
    end;
'''

