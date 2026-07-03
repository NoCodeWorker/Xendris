/-!
Strict-inclusion scaffolding for the Frontera C-Mayor bridge formalization.

This file proves only abstract consequences. A witness inside `D_LC` and
outside `D_CI` is assumed as a proposition; no physical example is encoded.
-/

import FrC.Subdomain

namespace FrC

def exists_LC_not_CI_for (O : Observer) : Prop :=
  Exists fun e : Event => D_LC O e /\ Not (D_CI O e)

def exists_LC_not_CI : Prop :=
  Exists fun O : Observer => Exists fun e : Event => D_LC O e /\ Not (D_CI O e)

def ProperSubdomainFor (O : Observer) : Prop :=
  (forall e : Event, D_CI O e -> D_LC O e) /\ exists_LC_not_CI_for O

def ProperSubdomainExists : Prop :=
  Exists fun O : Observer => ProperSubdomainFor O

theorem witness_for_observer_implies_proper_subdomain
    (O : Observer)
    (h : exists_LC_not_CI_for O) :
    ProperSubdomainFor O := by
  constructor
  · exact D_CI_subset_D_LC_for_observer O
  · exact h

theorem exists_LC_not_CI_implies_proper_subdomain_exists
    (h : exists_LC_not_CI) :
    ProperSubdomainExists := by
  rcases h with ⟨O, e, h_lc, h_not_ci⟩
  exists O
  exact witness_for_observer_implies_proper_subdomain O ⟨e, h_lc, h_not_ci⟩

end FrC
