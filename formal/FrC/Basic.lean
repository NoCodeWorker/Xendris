/-!
Frontera C-Mayor minimal bridge formalization.

This file defines only abstract types and predicates. It does not encode
physical claims, validation, novelty, or empirical support.
-/

namespace FrC

universe u

constant Observer : Type u
constant Event : Type u

constant A_c : Observer -> Event -> Prop
constant I_c : Observer -> Event -> Prop
constant M : Observer -> Event -> Prop
constant K : Observer -> Event -> Prop
constant R : Observer -> Event -> Prop

def D_LC (O : Observer) (e : Event) : Prop :=
  A_c O e

def D_CI (O : Observer) (e : Event) : Prop :=
  A_c O e /\ I_c O e /\ M O e /\ K O e /\ R O e

end FrC
