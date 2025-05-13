grammar govdsl;

// Parser rules
governance          : (scopes participants policy) EOF ;
policy              : (topLevelSinglePolicy | topLevelComposedPolicy) ;

// Top-level policies (with scope)
topLevelSinglePolicy    : policyType ID '{' scope decisionType policyParticipants? conditions? parameters? '}' ;
topLevelComposedPolicy  : 'ComposedPolicy' ID '{' scope order? phases '}' ;

// Nested policies (no scope)
nestedSinglePolicy      : policyType ID '{' decisionType policyParticipants? conditions? parameters? '}' ;
nestedComposedPolicy    : 'ComposedPolicy' ID '{' order? phases '}' ;

policyType          : 'MajorityPolicy' | 'LeaderDrivenPolicy' | 'AbsoluteMajorityPolicy' | 'ConsensusPolicy' | 'LazyConsensusPolicy' | 'VotingPolicy';

// Scope definition
scopes              : 'Scopes' ':' ( project | act | tsk) ; // Definition from upper element; but we can also define alone scopes
scope               : 'Scope' ':' ID ; // reference from policy
project             : 'Project' ID ('from' platform ':' repoID)? ('{' 'activities' ':' activity+ '}')? ;
platform            : 'GitHub' ;
repoID              : ID ('/' ID)? ; // owner/repo
act                 : 'Activity' activity ;
activity            : ID ('{' 'tasks' ':' task+ '}')? ;
tsk                 : 'Task' task ;
task                : ID (':' taskType)? ('{' taskContent '}')? ;
taskType            : 'Issue' | 'Pull request' | 'All' ; 
taskContent         : status | action | actionWithLabels ;
actionWithLabels    : action labels ;
status              : 'Status' ':' statusEnum ;
statusEnum          : 'completed' | 'accepted' | 'partial' ;
action              : 'Action' ':' actionEnum ;
actionEnum          : 'merge' | 'review' | 'release' ;
labels              : 'Labels' ':' ID (',' ID)* ;

// Decision type
decisionType        : 'DecisionType' 'as' (booleanDecision | stringList | elementList) ;
booleanDecision     : 'BooleanDecision' ;
stringList          : 'StringList' ':' ID (',' ID)* ;
elementList         : 'ElementList' ':' ID (',' ID)* ;

// Participants group
participants        : 'Participants' ':' ((roles individuals?) | (individuals roles?)) ;
policyParticipants  : 'Participant list' ':' partID (',' partID)* ;
partID              : ID hasRole? ;
roles               : 'Roles' ':' roleID (';' roleID)* ;
roleID              : ID ('composed of' ':' participantID (',' participantID)*)? ;
participantID       : ID  ;
individuals         : 'Individuals' ':' individualEntry (',' individualEntry)* ;
individualEntry     : individual | agent ;
individual          : participantID voteValue? ;
hasRole             : 'as' participantID ;
voteValue           : 'with vote value' FLOAT ;
agent               : '(Agent)' participantID voteValue? confidence? ;
confidence          : 'with confidence' FLOAT ;

// Conditions group
conditions          : 'Conditions' ':'  deadline? participantExclusion? minParticipant? vetoRight? passedTests? labelsCondition* ;
deadline            : 'Deadline' deadlineID ':' ( offset | date | (offset ',' date) ) ;
offset              : SIGNED_INT timeUnit ;
deadlineID          : ID ; // This allows the code to be more explainable in the listener
timeUnit            : 'days' | 'weeks' | 'months' | 'years' ;
date                : SIGNED_INT '/' SIGNED_INT '/' SIGNED_INT ; // DD/MM/YYYY; This can be improved with a lexer rule
participantExclusion: 'ParticipantExclusion' ':' participantID (',' participantID)* ;
minParticipant      : 'MinParticipants' ':' SIGNED_INT ;
vetoRight           : 'VetoRight' ':' participantID (',' participantID)* ; 
passedTests         : 'PassedTests' evaluationMode? ':' booleanValue ; // Does not make sense to declare this condition if booleanValue is false
evaluationMode      : ( 'pre' | 'post' | 'concurrent' ) ;
labelsCondition     : 'LabelCondition' evaluationMode? include?':' ID (',' ID)* ;
include             : 'include' | 'not';

// Parameters group
parameters          : 'Parameters' ':' (votParams | default) ;
votParams           :  ratio ; 
ratio               : 'ratio' FLOAT ; 
default             : 'default' nestedPolicy ;

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
ID              : [a-zA-Z_][a-zA-Z0-9_-]* ;
SIGNED_INT      : '-'? [0-9]+ ; // Just to cover the case where the user might use a negative number
FLOAT           : '-'? [0-9]+ '.' [0-9]+ ;
WS              : (' ' | '\t' | '\r'? '\n')+ -> skip ;