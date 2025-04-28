grammar govdsl;

// Parser rules
policy              : (topLevelSinglePolicy | topLevelComposedPolicy) EOF ;

// Top-level policies (with scope)
topLevelSinglePolicy    : policyType ID '{' scope participants? conditions? parameters? '}' ;
topLevelComposedPolicy  : 'ComposedPolicy' ID '{' scope order? phases '}' ;

// Nested policies (no scope)
nestedSinglePolicy      : policyType ID '{' participants? conditions? parameters? '}' ;
nestedComposedPolicy    : 'ComposedPolicy' ID '{' order? phases '}' ;

policyType          : 'MajorityPolicy' | 'LeaderDrivenPolicy' | 'AbsoluteMajorityPolicy' | 'ConsensusPolicy' | 'LazyConsensusPolicy' | 'VotingPolicy';

// Scope definition
scope               : 'Scope' ':' (project | activity | task) ;
project             : 'Project' ID ('from' platform ':' repoID)? ;
platform            : 'GitHub' ;
repoID              : ID ('/' ID)? ; // owner/repo
activity            : 'Activity' ID ;
task                : 'Task' ID (':' taskType)? '{' taskContent '}' ;
taskType            : 'Issue' | 'Pull request' | 'All' ; 
taskContent         : status | action | actionWithLabels ;
actionWithLabels    : action labels ;
status              : 'Status' ':' statusEnum ;
statusEnum          : 'completed' | 'accepted' | 'partial' ;
action              : 'Action' ':' actionEnum ;
actionEnum          : 'merge' | 'review' | 'release' ;
labels              : 'Labels' ':' ID (',' ID)* ;
// TODO: We could also use the "when" keyword to define the stage of the task (e.g., merge, review, etc.)

// Participants group
participants        : 'Participants' ':' ((roles individuals?) | (individuals roles?)) ;
roles               : 'Roles' ':' participantID (',' participantID)* ;
participantID       : ID  ;
individuals         : 'Individuals' ':' individualEntry (',' individualEntry)* ;
individualEntry     : individual | agent ;
individual          : participantID hasRole? voteValue? ;
hasRole             : 'as' participantID ;
voteValue           : 'with vote value' FLOAT ;
agent               : '(Agent)' participantID hasRole? voteValue? confidence? ;
confidence          : 'with confidence' FLOAT ;

// Conditions group
conditions          : 'Conditions' ':'  deadline? participantExclusion? minParticipant? vetoRight? passedTests? ;
deadline            : 'Deadline' deadlineID ':' ( offset | date | (offset ',' date) ) ;
offset              : SIGNED_INT timeUnit ;
deadlineID          : ID ; // This allows the code to be more explainable in the listener
timeUnit            : 'days' | 'weeks' | 'months' | 'years' ;
date                : SIGNED_INT '/' SIGNED_INT '/' SIGNED_INT ; // DD/MM/YYYY
participantExclusion: 'ParticipantExclusion' ':' participantID (',' participantID)* ;
minParticipant      : 'MinParticipants' ':' SIGNED_INT ;
vetoRight           : 'VetoRight' ':' participantID (',' participantID)* ; 
passedTests         : 'PassedTests' ':' booleanValue ; // Does not make sense to declare this condition if booleanValue is false

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
ID              : [a-zA-Z_][a-zA-Z0-9_]* ;
SIGNED_INT      : '-'? [0-9]+ ; // Just to cover the case where the user might use a negative number
FLOAT           : '-'? [0-9]+ '.' [0-9]+ ;
WS              : (' ' | '\t' | '\r'? '\n')+ -> skip ;