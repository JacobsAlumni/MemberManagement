import make_chart, { as_bar_series, format_value } from "./make_chart";

const totalElement = document.getElementById('total') as HTMLSpanElement;

const setupElement = document.getElementById('setup') as HTMLDivElement;
const approvalElement = document.getElementById('approval') as HTMLDivElement;
const autoElement = document.getElementById('auto') as HTMLDivElement;

const tierElement = document.getElementById('tier') as HTMLDivElement;
const categoryElement = document.getElementById('category') as HTMLDivElement;

const degreeElement = document.getElementById('degree') as HTMLDivElement;
const collegeElement = document.getElementById('college') as HTMLDivElement;

const graduationElement = document.getElementById('graduation') as HTMLDivElement;
const majorElement = document.getElementById('major') as HTMLDivElement;

const genderElement = document.getElementById('gender') as HTMLDivElement;
const atlasElement = document.getElementById('atlas') as HTMLDivElement;

const COLORS_YES_NO = [['yes', '#008000'], ['no', '#800080']] as Array<[string, string]>;

function write_stats(stats: PortalStats) {
    totalElement.innerText = format_value(stats.total);

    make_chart('pie', setupElement, stats.setup, COLORS_YES_NO);
    make_chart('pie', approvalElement, stats.approval, COLORS_YES_NO);
    make_chart('pie', autoElement, stats.autocreated, COLORS_YES_NO);

    make_chart('pie', tierElement, stats.tier, Object.keys(stats.tier),
        (name: string) => name.split(/\s/)[0],
    );
    make_chart('pie', categoryElement, stats.category, Object.keys(stats.category),
        (name: string) => name.split(/\s/)[0],
    );

    make_chart('pie', degreeElement, stats.degree, Object.keys(stats.degree),
        {
            'Foundation Year': 'FY',
            'Bachelor of Arts': 'BA',
            'Bachelor of Science': 'BSc',
            'Master of Arts': 'MA',
            'Master of Science': 'MSc',
        }
    );
    make_chart('pie', collegeElement, stats.college, [
        ['Nordmetall', 'yellow'],
        ['Krupp', 'red'],
        ['Mercator', 'blue'],
        ['College III', 'darkgreen'],
        ['College V', 'black']
    ]);

    make_chart('pie', graduationElement, stats.graduation, Object.keys(stats.graduation),
        (name: string) => name.startsWith('Class') ? name.split(/\s/).reverse()[0] : 'Unknown',
        as_bar_series({ cull: true, sort: 'label' }),
    );

    make_chart('pie', majorElement, stats.major, Object.keys(stats.major),
        {
            'Other (Please specify in comments)': 'Unknown',
        },
        as_bar_series({ cull: true, sort: 'count', noticks: true, }),
    );

    make_chart('pie', genderElement, stats.gender, [
        ['Prefer not to say', 'black'],
        ['Non-binary', 'yellow'],
        ['Female', 'red'],
        ['Male', 'blue'],
    ]);
    make_chart('pie', atlasElement, stats.atlas, COLORS_YES_NO);
}

document.addEventListener('DOMContentLoaded', () => {
    write_stats(window.stats);
});