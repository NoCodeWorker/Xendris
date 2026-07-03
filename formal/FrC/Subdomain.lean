/-!
Definitional subdomain result for the Frontera C-Mayor bridge formalization.

The theorem below states only that the abstract `D_CI` predicate implies the
abstract `D_LC` predicate by construction.
-/

import FrC.Basic

namespace FrC

theorem D_CI_subset_D_LC (O : Observer) (e : Event) :
    D_CI O e -> D_LC O e := by
  intro h
  exact h.1

theorem D_CI_subset_D_LC_for_observer (O : Observer) :
    forall e : Event, D_CI O e -> D_LC O e := by
  intro e h
  exact D_CI_subset_D_LC O e h

end FrC
