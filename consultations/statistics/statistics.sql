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


-- emails of active members who haven't voted in consultation 1

\copy (
select distinct m.email 
from    members_member m 
        left outer join consultations_vote v on m.id = v.member_id 
where m.is_active = 't' and v.id is null) 
to '~/Desktop/consultation_1_non_voters.csv' CSV FORCE QUOTE email

\copy (select distinct m.email from members_member m left outer join consultations_vote v on m.id = v.member_id where m.is_active = 't' and v.id is null) to '~/Desktop/consultation_1_non_voters.csv' CSV FORCE QUOTE email

-- import CSV of emails to email targets
create table non_voters (email citext);
\copy non_voters from '~/Desktop/consultation_1_non_voters.csv' with CSV
insert into mxv_emailtarget (email) select email from non_voters;
drop table non_voters;

-- consultation 1 votes

\copy (
select * from crosstab(
    'select distinct m.name, m.email, q.number, ch.display_order
    from    members_member m 
            inner join consultations_vote v on m.id = v.member_id 
            inner join consultations_consultation co on v.consultation_id = co.id
            inner join consultations_answer a on v.id = a.vote_id 
            inner join consultations_choice ch on a.choice_id = ch.id
            inner join consultations_question q on ch.question_id = q.id        
    where co.id = 1
    order by 1,2',
    $$values ('1'::text), ('2'::text), ('3'::text), ('4'::text), ('5'::text), ('6'::text)$$ 
    ) as ct("Name" text, "Email" text, "Q1" int, "Q2" int, "Q3" int, "Q4" int, "Q5" int, "Q6" int)
) to '~/Desktop/consultation_1_voters_and_choices.csv' CSV 

\copy (select * from crosstab('select distinct m.name, m.email, q.number, ch.display_order from members_member m inner join consultations_vote v on m.id = v.member_id inner join consultations_consultation co on v.consultation_id = co.id inner join consultations_answer a on v.id = a.vote_id inner join consultations_choice ch on a.choice_id = ch.id inner join consultations_question q on ch.question_id = q.id where co.id = 1 order by 1,2', $$values ('1'::text), ('2'::text), ('3'::text), ('4'::text), ('5'::text), ('6'::text)$$ ) as ct("Name" text, "Email" text, "Q1" int, "Q2" int, "Q3" int, "Q4" int, "Q5" int, "Q6" int)) to '~/Desktop/consultation_1_voters_and_choices.csv' CSV 


-- voters with choices <> 6
select email, count(*) from members_member m inner join consultations_vote v on m.id = v.member_id inner join consultations_consultation co on v.consultation_id = co.id inner join consultations_answer a on v.id = a.vote_id inner join consultations_choice ch on a.choice_id = ch.id inner join consultations_question q on ch.question_id = q.id where co.id = 1 group by email having count(*) <> 6 order by count(*) desc;

