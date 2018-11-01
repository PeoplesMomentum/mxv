-- consultation 1 voters

\copy (
select distinct m.name, m.email 
from    members_member m 
        inner join consultations_vote v on m.id = v.member_id 
        inner join consultations_consultation c on v.consultation_id = c.id
        inner join consultations_answer a on v.id = a.vote_id 
where c.id = 1) 
to '~/Desktop/consultation_1_voters.csv' CSV FORCE QUOTE name, email

\copy (select distinct m.name, m.email from members_member m inner join consultations_vote v on m.id = v.member_id inner join consultations_consultation c on v.consultation_id = c.id inner join consultations_answer a on v.id = a.vote_id where c.id = 1) to '~/Desktop/consultation_1_voters.csv' CSV FORCE QUOTE name, email



-- active members

\copy (
select distinct m.name, m.email 
from    members_member m 
where m.is_active = 't') 
to '~/Desktop/active_members.csv' CSV FORCE QUOTE name, email

\copy (select distinct m.name, m.email from members_member m where m.is_active = 't') to '~/Desktop/active_members.csv' CSV FORCE QUOTE name, email


-- emails of members who haven't voted in consultation 1

\copy (
select distinct m.email 
from    members_member m 
        left outer join consultations_vote v on m.id = v.member_id 
where v.id is null) 
to '~/Desktop/consultation_1_non_voters.csv' CSV FORCE QUOTE email

\copy (select distinct m.email from members_member m left outer join consultations_vote v on m.id = v.member_id where v.id is null) to '~/Desktop/consultation_1_non_voters.csv' CSV FORCE QUOTE email

-- import CSV of emails to email targets
create table non_voters (email citext);
\copy non_voters from '~/Desktop/consultation_1_non_voters.csv' with CSV
insert into mxv_emailtarget (email) select email from non_voters;
drop table non_voters;