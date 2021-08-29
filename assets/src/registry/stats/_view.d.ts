// This interface should be kept in sync with alumni/admin/stats.py
interface PortalStats {
    total: number;

    approval: _YesNoStat;
    setup: _YesNoStat;
    autocreated: _YesNoStat;

    category: _Stat< 'Alum (Former Student)' | 'Faculty Or Staff' | 'Friend Of The Association' >;
    tier: _Stat< 'Contributor – Standard membership for 39€ p.a.' | 'Starter – Free Membership for 0€ p.a.' | 'Patron – Premium membership for 249€ p.a.' >;
    atlas: _YesNoStat;
    degree: _Stat< 'Foundation Year' | 'Bachelor of Arts' | 'Bachelor of Science' | 'Master of Arts' | 'Master of Science' | 'PhD' | 'MBA' >;
    graduation: _Stat< 'Other (Please specify in comments)' | 'Class of 2004' | 'Class of 2005' | 'Class of 2006' | 'Class of 2007' | 'Class of 2008' | 'Class of 2009' | 'Class of 2010' | 'Class of 2011' | 'Class of 2012' | 'Class of 2013' | 'Class of 2014' | 'Class of 2015' | 'Class of 2016' | 'Class of 2017' | 'Class of 2018' | 'Class of 2019' | 'Class of 2020' | 'Class of 2021' | 'Class of 2022' | 'Class of 2023' | 'Class of 2024' | 'Class of 2025' >;
    major: _Stat< 'Applied Computational Mathematics (ACM)' | 'Applied Physics and Mathematics' | 'Astroparticle Physics' | 'Attitude Formation' | 'Biochemical Engineering' | 'Biochemistry' | 'Biochemistry and Cell Biology (BCCB)' | 'Bioinformatics and Computational Biology' | 'Biological Recognition' | 'Biology' | 'Biology/Neuroscience' | 'Biotechnology' | 'Buisness Administration' | 'Changing Lives in Changing Socio-Cultural Contexts' | 'Chemistry' | 'Communications' | 'Comparative PolitIcs and Sociology' | 'Computational Life Science' | 'Computer Science' | 'Data Engineering' | 'Earth and Environmental Sciences' | 'Earth and Space Sciences' | 'Electrical and Computer Engineering' | 'Electrical Engineering and Computer Science' | 'European Utility Management' | 'Geo-Ocean Dynamics' | 'Geosciences and Astrophysics' | 'Global Economics and Management (GEM)' | 'Global Governance and Regional Integration' | 'Global Visual Communication' | 'History' | 'History and Theory of Art and Literature' | 'Humanities' | 'Industrial Engineering and Management' | 'Information Management and Systems (IMS)' | 'Integrated Cultural Studies' | 'Integrated Environmental Studies' | 'Integrated Social and Cognitive Psychology (ISCP)' | 'Integrated Social Sciences' | 'Intelligent Mobile Systems' | 'Intercultural Humanities' | 'Intercultural Relations and Behaviour (IRB)' | 'International Relations: Global Governance and Social Theory' | 'International Business Administration' | 'International Communication' | 'International History and Politics' | 'International Logistics Engineering and Management (ILME)' | 'International Politics and History (IPH)' | 'International Relations' | 'Life-Course and Lifespan Dynamics' | 'Lifelong Learning' | 'Marine Microbiology' | 'Mathematics' | 'Medical Chemistry and Chemical Biology' | 'Medical Natural Sciences' | 'Modern Global History' | 'Molecular Life Science' | 'Nanomolecular Sciences' | 'Neuroscience' | 'Physics' | 'Political Economy & Public Policy' | 'Productive Adult Development' | 'Psychology' | 'Smart Systems' | 'Supply Chain Engineering and Management' | 'Visual Communication and Expertise' | 'Welfare State, Inequality and Quality of Life' | 'Other (Please specify in comments)' >;
    gender: _Stat< 'Female' | 'Male' | 'Non-binary' | 'Prefer not to say' >;
    college: _Stat< 'Krupp' | 'Mercator' | 'College III' | 'Nordmetall' | 'College V' >;
}

type _Stat<T extends string> = Record<T, number>
type _YesNoStat = _Stat<"yes" | "no">

interface Window {
    readonly stats: PortalStats;
}
