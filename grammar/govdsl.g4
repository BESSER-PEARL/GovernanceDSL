grammar govdsl;

// Parser rules
policy              : policyContent EOF ;
policyContent       : singlePolicy | phasedPolicy ;
singlePolicy        : 'Policy' ID '{'  attributesSingle*  '}' ;
phasedPolicy        : 'PhasedPolicy' ID '{'  attributesPhased*  '}' ;
attributesSingle    : scopes | participants | conditions | rules ;
attributesPhased    : order | phases ;
// Scope group
scopes              : 'Scope' ':'  (project | activity | task) ;
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
participants        : 'Participants' ':' roles | individuals ;
roles               : 'Roles' ':' participantID (',' participantID)* ;
participantID       : ID  ;
individuals         : 'Individuals' ':' individualID (',' individualID)* ;
individualID        : participantID hasRole? ;
hasRole             : 'as' participantID ;
// Conditions group
conditions          : 'Conditions' ':'  deadline? votingCondition? ratio? ;
deadline            : 'Deadline' deadlineID ':' ( offset | date | (offset ',' date) ) ;
offset              : SIGNED_INT timeUnit ;
deadlineID          : ID ; // This allows the code to be more explainable in the listener
timeUnit            : 'days' | 'weeks' | 'months' | 'years' ;
date                : SIGNED_INT '/' SIGNED_INT '/' SIGNED_INT ; // DD/MM/YYYY
votingCondition     : 'VotingCondition' voteConditionID ':' (minVotes | ratio | (minVotes ',' ratio)) ;  // TODO: Change to a whole condition, where we can have minVotes and/or ratio
voteConditionID     : ID ;
minVotes            : 'minVotes' SIGNED_INT ; 
ratio               : 'ratio' FLOAT ; 
// Rules group
rules               : 'Rules' ':'  rule+ ;
rule                : ruleID ':' ruleType '{'  ruleContent  '}'  ; // ruleContent depending on ruleType
ruleID              : ID ;
ruleType            : 'Majority' | 'LeaderDriven' | 'Ratio' ;
ruleContent         : people? rangeType? ruleConditions? default? ; // TODO: Propose alternative?
// collaborationID     : 'Issue' | 'Pull request' | 'All';
// stage                : 'when' taskID ; // TODO: Refactor on event-based?
// taskID              : 'Task Review' | 'Patch Review' | 'Release' | 'All' ;
people              : 'people' participantID (',' participantID)* ;
rangeType           : 'range' rangeID ;
rangeID             : 'Present' | 'Qualified' ;
ruleConditions      : 'conditions' ID (',' ID)* ;
default             : ('default' ruleID) ; // LD
// Phased policy 
order               : 'Order' ':' orderType ('{' orderMode '}')? ; 
orderType           : 'Sequential' | 'Parallel' ;
orderMode           : 'exclusive' | 'inclusive' ;
phases              : 'Phases' '{' (singlePolicy | phasedPolicy)+ '}' ;

// Lexer rules
ID              : [a-zA-Z_][a-zA-Z0-9_]* ;
SIGNED_INT      : '-'? [0-9]+ ; // Just to cover the case where the user might use a negative number
FLOAT           : [0-9]+ '.' [0-9]+ ;
// NL              : ('\r'? '\n')+ ;
WS              : (' ' | '\t' | '\r'? '\n')+ -> skip ;