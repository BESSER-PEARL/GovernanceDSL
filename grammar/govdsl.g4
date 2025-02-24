grammar govdsl;

// Parser rules
policy              : 'Policy' ID '{'   attributes*  '}' EOF;
attributes          : project | participants | conditions | rules | scope ;
// Project group
project             : ID ':' 'Project' '{'   activity*  '}' ;
activity            : ID ':' 'Activity' '{'  task*  '}' ;
task                : ID ':' 'Task' ; 
// Participants group
participants        : 'Participants' ':' roles | individuals ;
roles               : 'Roles' ':' participantID (',' participantID)* ;
participantID       : ID ;
individuals         : 'Individual' ':' participantID (',' participantID)* ;
// Conditions group
conditions          : 'Conditions' ':'  deadline+ ;
deadline            : deadlineID ':' SIGNED_INT timeUnit ;
deadlineID          : ID ; // This allows the code to be more explainable in the listener
timeUnit            : 'days' | 'weeks' | 'months' | 'years' ;
// Rules group
rules               : 'Rules' ':'  rule+ ;
rule                : ruleID ':' ruleType '{'  ruleContent  '}'  ; // ruleContent depending on ruleType
ruleID              : ID ;
ruleType            : 'Majority' | 'LeaderDriven' | 'Ratio' ;
ruleContent         : people? rangeType? minVotes? ratio? ('deadline' deadlineID)? default? ; // TODO: Propose alternative?
// collaborationID     : 'Issue' | 'Pull request' | 'All';
// stage                : 'when' taskID ; // TODO: Refactor on event-based?
// taskID              : 'Task Review' | 'Patch Review' | 'Release' | 'All' ;
people              : 'people' participantID (',' participantID)* ;
rangeType           : 'range' rangeID ;
rangeID             : 'Present' | 'Qualified' ;
minVotes            : 'minVotes' SIGNED_INT ;  // Maj
ratio               : 'ratio' FLOAT ; // Maj
default             : ('default' ruleID) ; // LD
// Scope group
scope               : 'Scope' ':' ID ;
// Phased policy TODO: Implement
phases              : 'phases' '{' ruleID+ '}' ; // Phased


// Lexer rules
ID              : [a-zA-Z_][a-zA-Z0-9_]* ;
SIGNED_INT      : '-'? [0-9]+ ; // Just to cover the case where the user might use a negative number
FLOAT           : [0-9]+ '.' [0-9]+ ;
// NL              : ('\r'? '\n')+ ;
WS              : (' ' | '\t' | '\r'? '\n')+ -> skip ;