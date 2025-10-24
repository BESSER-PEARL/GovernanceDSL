grammar govdsl;

// Parser rules
governance          : (scopes participants policy+) EOF ;
policy              : (topLevelSinglePolicy | topLevelComposedPolicy) ;

// Top-level policies (with scope)
topLevelSinglePolicy    : policyType ID '{' scope decisionType policyParticipants communicationChannel? conditions? parameters? '}' ;
topLevelComposedPolicy  : 'ComposedPolicy' ID '{' scope order? phases '}' ;

// Nested policies (no scope)
nestedSinglePolicy      : policyType ID '{' decisionType policyParticipants communicationChannel? conditions? parameters? '}' ;
nestedComposedPolicy    : 'ComposedPolicy' ID '{' order? phases '}' ;

policyType          : 'MajorityPolicy' | 'LeaderDrivenPolicy' | 'AbsoluteMajorityPolicy' | 'ConsensusPolicy' | 'LazyConsensusPolicy' | 'VotingPolicy';

// Scope definition
scopes              : 'Scopes' ':' ( projects | activities | tasks)+ ; // Definition from upper element; but we can also define alone scopes
scope               : 'Scope' ':' ID ; // reference from policy
projects            : 'Projects' ':' project+ ;
project             : ID ('from' platform ':' repoID)? ('{' 'Activities' ':' activity+ '}')? ;
platform            : 'GitHub' | 'GitLab' ;
repoID              : ID ; // owner/repo
activities          : 'Activities' ':' activity+ ;
activity            : ID ('{' 'Tasks' ':' task+ '}')? ;
tasks               : 'Tasks' ':' task+ ;
task                : ID (':')? (patchTask | memberTask )? ;
patchTask           : patchTaskType ('{' patchTaskContent '}')? ;
memberTask          : 'MemberLifecycle' ('{' memberTaskContent '}')? ;
patchTaskType       : 'Issue' | 'Pull request' | 'All' ; //TODO: Update with Patch / PR
patchTaskContent    : status | patchAction | actionWithLabels ;
actionWithLabels    : patchAction labels ;
memberTaskContent   : memberAction ;
memberAction        : 'Action' ':' memberActionEnum ;
memberActionEnum    : 'onboard' | 'remove' ;
status              : 'Status' ':' statusEnum ;
statusEnum          : 'completed' | 'accepted' | 'partial' ;
patchAction         : 'Action' ':' patchActionEnum ;
patchActionEnum     : 'merge' | 'review' | 'release' ;
labels              : 'Labels' ':' ID (',' ID)* ;

// Decision type
decisionType        : 'DecisionType' 'as' (booleanDecision | stringList | elementList) ;
booleanDecision     : 'BooleanDecision' ;
stringList          : 'StringList' ':' ID (',' ID)* ;
elementList         : 'ElementList' ':' ID (',' ID)* ;

// Communication channel
communicationChannel: 'CommunicationChannel' ':' ID ;

// Participants group
participants        : 'Participants' ':' (roles | individuals | profiles)+ ;
roles               : 'Roles' ':' role (',' role)* ;
role                : ID ('{' voteValue?'}')? ;
individuals         : 'Individuals' ':' individualEntry ((',')? individualEntry)* ;
individualEntry     : individual | agent ;
individual          : ID ('{' voteValue? (',')? withProfile? (',')? withRole? '}')? ; 
voteValue           : 'vote value' ':' FLOAT ;
withProfile         : 'profile' ':' ID ;
withRole            : 'role' ':' ID (',' ID)* ;
agent               : '(Agent)' ID ('{' voteValue? (',')? confidence? (',')? autonomyLevel? (',')? explainability? (',')? withRole? '}')? ;
confidence          : 'confidence' ':' FLOAT ;
autonomyLevel       : 'autonomy level' ':' FLOAT ;
explainability      : 'explainability' ':' FLOAT ;
profiles            : 'Profiles' ':' profile ((',')? profile)* ;
profile             : ID '{' profileAttr (','? profileAttr)* '}';
profileAttr         : gender | race | language ;
gender              : 'gender' ':' ID ;
race                : 'race' ':' ID ;
language            : 'language' ':' ID ;
policyParticipants  : 'Participant list' ':' partID (',' partID)* ;
partID              : ID hasRole? ;
hasRole             : 'as' ID ;

// Conditions group
conditions          : 'Conditions' ':'  deadline? minDecisionTime? participantExclusion? minParticipant? vetoRight? appealRight? checkCiCd? minTime? labelsCondition* ; // + extension
deadline            : 'Deadline' deadlineID? ':' ( offset | date | (offset ',' date) ) ;
minDecisionTime     : 'MinDecisionTime' ID? ':' ( offset | date | (offset ',' date) ) ;
offset              : SIGNED_INT timeUnit ;
deadlineID          : ID ; // This allows the code to be more explainable in the listener
timeUnit            : 'days' | 'weeks' | 'months' | 'years' ;
date                : SIGNED_INT '/' SIGNED_INT '/' SIGNED_INT ; // DD/MM/YYYY; This can be improved with a lexer rule
participantExclusion: 'ParticipantExclusion' ':' ID (',' ID)* ; // TODO: ID | 'PRAuthor' | 'RepoOwner' 
minParticipant      : 'MinParticipants' ':' SIGNED_INT ;
vetoRight           : 'VetoRight' ':' ID (',' ID)* ; 
appealRight         : 'AppealRight' ':' '{' 'Appealers' ':' ID (',' ID)* ','? 'Policy' ':' (nestedPolicy | policyReference) '}' ;
checkCiCd           : 'CheckCiCd' evaluationMode? ':' booleanValue ; // Does not make sense to declare this condition if booleanValue is false
minTime             : 'MinTime' evaluationMode? 'of' activityBool ':' offset ;
activityBool        : 'Activity' | 'InActivity' ;
evaluationMode      : ( 'pre' | 'post' | 'concurrent' ) ;
labelsCondition     : 'LabelCondition' evaluationMode? include?':' ID (',' ID)* ;
include             : 'include' | 'not';

// Parameters group
parameters          : 'Parameters' ':' (votParams | default | fallback) ;
votParams           :  ratio ; 
ratio               : 'ratio' ':' FLOAT ; 
default             : 'default' ':' (nestedPolicy | policyReference) ;
fallback            : 'fallback' ':' (nestedPolicy | policyReference) ;
policyReference     : ID ;

// Phased policy 
order               : 'Order' ':' ( orderType orderMode carryOver? ) ; 
orderType           : 'Execution' ':' orderTypeValue ;
orderTypeValue      : 'sequential' | 'parallel' ;
orderMode           : 'RequireAll' ':' booleanValue ;
carryOver           : 'CarryOver' ':' booleanValue ;
booleanValue        : 'true' | 'false' ;
phases              : 'Phases' '{' nestedPolicy+ '}' ;
nestedPolicy        : nestedSinglePolicy | nestedComposedPolicy ;

// Lexer rules
ID              : [a-zA-Z_][a-zA-Z0-9_/-]* ;
// LABEL           : [a-zA-Z_][a-zA-Z0-9_/:-]* ; // Labels can contain '/', '-', and ':'
SIGNED_INT      : '-'? [0-9]+ ; // Just to cover the case where the user might use a negative number
FLOAT           : '-'? [0-9]+ '.' [0-9]+ ;
WS              : (' ' | '\t' | '\r'? '\n')+ -> skip ;