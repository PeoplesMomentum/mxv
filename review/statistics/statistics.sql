select  count(*) 
from    review_amendment a 
        inner join review_proposal p on a.proposal_id = p.id 
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2';

select  count(*) from (
select  distinct a.created_by_id 
from    review_amendment a 
        inner join review_proposal p on a.proposal_id = p.id 
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2') query;

select  count(*) 
from    review_comment c 
        inner join review_proposal p on c.proposal_id = p.id 
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2';

select  count(*) from (
select  distinct c.created_by_id
from    review_comment c 
        inner join review_proposal p on c.proposal_id = p.id 
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2') query;

select  count(*) 
from    review_proposal p
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2';

select  count(*) from (
select  distinct p.created_by_id
from    review_proposal p
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2') query;

select  count(*) 
from    review_nomination n 
        inner join review_proposal p on n.proposal_id = p.id 
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2';

select  count(*) from (
select  distinct n.nominated_by_id
from    review_nomination n 
        inner join review_proposal p on n.proposal_id = p.id 
        inner join review_theme th on p.theme_id = th.id 
        inner join review_track tr on th.track_id = tr.id 
where   tr.name = 'Track 2') query;

select  count(*)
from    members_member
where   is_active = 't';

select  count(*)
from    members_member;

select  count(*) from (
select  distinct v.member_id
from    review_vote v
        inner join review_answer a on v.id = a.vote_id
        inner join review_trackvoting tv on v.track_voting_id = tv.id
        inner join review_track tr on tv.track_id = tr.id 
where   tr.name = 'Track 2') query;

\copy (select distinct m.name, m.email from members_member m inner join review_vote v on m.id = v.member_id inner join review_answer a on v.id = a.vote_id inner join review_trackvoting tv on v.track_voting_id = tv.id inner join review_track tr on tv.track_id = tr.id where tr.name = 'Track 2') to 'track 2 voters.csv' with CSV

