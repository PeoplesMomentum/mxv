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

                 email                 | count 
---------------------------------------+-------
 tepeyurt@gmail.com                    |    10
 momentum@focusfree.com                |    10
 wendykimber65@gmail.com               |     9
 koncarvanda@gmail.com                 |     8
 ellen_morrison@hotmail.co.uk          |     5
 henry.fowler@hotmail.co.uk            |     5
 steven.blackwell@gmail.com            |     5
 khanley@blueyonder.co.uk              |     5
 davidjbohannan@gmail.com              |     5
 robinjulieandrosie@tiscali.co.uk      |     5
 p.f.cuthbert@btinternet.com           |     5
 elicens@gmail.com                     |     5
 catherine@londonmeditationproject.org |     5
 sossity@live.co.uk                    |     5
 xclive@tiscali.co.uk                  |     5
 suhaabdul@hotmail.com                 |     5
 colima@btopenworld.com                |     5
 martinbbailey@gmail.com               |     5
 picture.uk@gmail.com                  |     5
 TonyRobinsonOBE@gmail.com             |     5
 billy_harrington_roberts@hotmail.com  |     5
 jrmansilla@tiscali.co.uk              |     5
 stparsons@hotmail.co.uk               |     5
 jeremy.kearney@blueyonder.co.uk       |     5
 Nick@thesussexproducecompany.co.uk    |     5
 abbey-rh@hotmail.com                  |     5
 pcruick87@gmail.com                   |     5
 robin@paice.org.uk                    |     5
 roy185m@gmail.com                     |     5
 lauriemn27@gmail.com                  |     5
 leigh-drennan@hotmail.co.uk           |     5
 johnkmiddycsniclp@btinternet.com      |     5
 subs@khobbs.org                       |     5
 prestonclaire@hotmail.com             |     5
 kthkeith@msn.com                      |     5
 jolainscough@gmail.com                |     5
 peterecooper@btinternet.com           |     5
 hillsidepaul@gmail.com                |     5
 joepiercy@hotmail.co.uk               |     5
 celestine.boyle@gmail.com             |     5
 pinesylar@gmail.com                   |     5
 psrnnl@gmail.com                      |     5
 brinleydavies@gmail.com               |     5
 sarah.hillier4@btinternet.com         |     5
 coestreicher@clara.co.uk              |     5
 itareus@hotmail.com                   |     5
 angieogrady@mail.com                  |     5
 Merriel.Waggoner@btinternet.com       |     5
 gloria.george@btinternet.com          |     5
 christine.pettengell@ntlworld.com     |     5
 watki.labour@gmail.com                |     5
 mlevansyoung@aol.com                  |     5
 harptreemartins@btinternet.com        |     5
 ellyannab@hotmail.com                 |     5
 dembonet@aol.com                      |     5
 vpmills@outlook.com                   |     5
 john-allen1@hotmail.com               |     5
 dragicevic.tom@gmail.com              |     5
 gulonline@gmx.com                     |     5
 steve@holdenweb.com                   |     5
 jasmith93@live.co.uk                  |     5
 john.graves@live.co.uk                |     5
 aroberts@gmail.com                    |     5
 joycehanna@virginmedia.com            |     5
 mayaevans@fastmail.co.uk              |     5
 e.stockhammer@kingston.ac.uk          |     5
 peter.elliott@lancaster.ac.uk         |     5
 mpgroombridge@gmail.com               |     5
 cstaylor7@gmail.com                   |     5
 samswash@googlemail.com               |     5
 subarton@btinternet.com               |     5
 frenchquentin@gmail.com               |     5
 sm014b3939@blueyonder.co.uk           |     5
 kaleblloyd83@gmail.com                |     5
 ricardo@gladwell.me                   |     5
 chrisbarson@hotmail.co.uk             |     5
 tomcoogan5000@gmail.com               |     5
 shaunjreidy@googlemail.com            |     5
 katiemoudry@gmail.com                 |     5
 david@pharmasee3000.co.uk             |     5
 sbpearce@btinternet.com               |     5
 vkmitchell79@gmail.com                |     5
 quinnpohl@outlook.com                 |     5
 Matthewcorrall@outlook.com            |     5
 rle.massey55@gmail.com                |     4
 getianneal@gmail.com                  |     4
 sarah.friday@hotmail.co.uk            |     4
 pascalebrad@aol.com                   |     4
 hedleybashforth@gmail.com             |     4
 rshid.dalla@gmail.com                 |     2
 macgraville@gmail.com                 |     1
 jeananncowsill@gmail.com              |     1
 stevensaxby@btinternet.com            |     1
(93 rows)
