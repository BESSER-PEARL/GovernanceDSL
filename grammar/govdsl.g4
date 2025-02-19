grammar govdsl;

// Parser rules
project             : 'Project' ID '{'   attributes*  '}' EOF;
attributes           : roles | deadlines | rules ;
roles               : 'Roles' ':' roleID (',' roleID)*  ;
roleID              : ID ; 
deadlines           : 'Deadlines' ':'  deadline+  ;
deadline            : deadlineID ':' SIGNED_INT timeUnit ;
deadlineID          : ID ;
rules               : 'Rules' ':'  rule+ ;
rule                : ruleID ':' ruleType '{'  ruleContent  '}'  ; // ruleContent depending on ruleType
ruleID              : ID ;
ruleContent         : appliedTo? stage? people? rangeType? minVotes? ratio? ('deadline' deadlineID)? default? phases? ; // TODO: Propose alternative?
appliedTo           : 'applied to' collaborationID ;
collaborationID     : 'Issue' | 'Pull request' | 'All';
stage               : 'when' stageID ;
stageID             : 'Task Review' | 'Patch Review' | 'Release' | 'All' ;
people              : 'people' roleID (',' roleID)* ;
rangeType           : 'range' rangeID ;
rangeID             : 'Present' | 'Qualified' ;
minVotes            : 'minVotes' SIGNED_INT ; 
default             : ('default' ruleID) ;
ratio               : 'ratio' FLOAT ;
phases              : 'phases' '{' ruleID+ '}' ;
timeUnit            : 'days' | 'weeks' | 'months' | 'years' ;
ruleType            : 'Majority' | 'LeaderDriven' | 'Ratio' | 'Phased' ;

// Lexer rules
ID              : [a-zA-Z_][a-zA-Z0-9_]* ;
SIGNED_INT      : '-'? [0-9]+ ; // Just to cover the case where the user might use a negative number
FLOAT           : [0-9]+ '.' [0-9]+ ;
// NL              : ('\r'? '\n')+ ;
WS              : (' ' | '\t' | '\r'? '\n')+ -> skip ;