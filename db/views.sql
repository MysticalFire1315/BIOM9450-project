create or replace view researchers_list(id, firstname, lastname, dob, sex) as
select p.* from people p join researchers r on p.id = r.people_id;

create or replace view oncologists_list(id, firstname, lastname, dob, sex) as
select p.* from people p join oncologists o on p.id = o.people_id;