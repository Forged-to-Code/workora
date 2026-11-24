-- Optional: create an employer through signup first; replace the placeholder UUID
-- with that employer's auth user ID. All these listings are fictional.
-- Run manually only in a sandbox project.
insert into public.jobs(employer_id,title,employer,category,area,lat,lng,wage,frequency,type,hours,skills,description,vacancies)
select id,'Demo Site Electrician','Demo Greenline Electricals','Electrician','Vajarahalli',12.884,77.545,900,'daily','Full-time','9 AM – 6 PM',array['Electrical work','Safety'],'Fictional sample listing for a hackathon demonstration.',2 from public.profiles where id='00000000-0000-0000-0000-000000000000' and role='employer';
insert into public.jobs(employer_id,title,employer,category,area,lat,lng,wage,frequency,type,hours,skills,description,vacancies)
select id,'Demo Plumbing Technician','Demo Metro Pipe Services','Plumber','Kanakapura Road',12.890,77.552,850,'daily','Full-time','9 AM – 6 PM',array['Plumbing'],'Fictional sample listing for a hackathon demonstration.',1 from public.profiles where id='00000000-0000-0000-0000-000000000000' and role='employer';
