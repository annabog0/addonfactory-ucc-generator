# This script triggers tests on appropriate codeline (passed from command line)

function invoke_plan()
{
curl -X POST --user dzakharov:bamboo -d bamboo.variable.CODELINE=$CODELINE http://app-bamboo/rest/api/latest/queue/${1}?os_authType=basic
}

invoke_plan SOLNSHAREDCOMPONENTS-SOLNSHAREDCOMPONENTSJSLINT
invoke_plan SOLNSHAREDCOMPONENTS-SOLNSHAREDCOMPONENTSSTATICJSLINT
invoke_plan SOLNSHAREDCOMPONENTS-SOLNSHAREDCOMPONENTSUNITCURRGA
invoke_plan SOLNSHAREDCOMPONENTS-SHAREDCOMPONENTSUNITNEXT