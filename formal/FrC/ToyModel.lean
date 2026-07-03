/-!
Abstract toy witness for strict inclusion.

This file assumes a toy observer and event. The assumptions state that the
event is causally accessible while transmissible information fails. This is a
formal witness only; it does not encode or validate a physical system.
-/

import FrC.StrictInclusion

namespace FrC

constant O0 : Observer
constant e0 : Event

axiom toy_A_c_O0_e0 : A_c O0 e0
axiom toy_not_I_c_O0_e0 : Not (I_c O0 e0)

theorem toy_e0_in_D_LC : D_LC O0 e0 := by
  exact toy_A_c_O0_e0

theorem toy_e0_notin_D_CI : Not (D_CI O0 e0) := by
  intro h
  exact toy_not_I_c_O0_e0 h.2.1

theorem toy_exists_LC_not_CI_for_O0 : exists_LC_not_CI_for O0 := by
  exact Exists.intro e0 ⟨toy_e0_in_D_LC, toy_e0_notin_D_CI⟩

theorem toy_proper_subdomain_for_O0 : ProperSubdomainFor O0 := by
  exact witness_for_observer_implies_proper_subdomain O0 toy_exists_LC_not_CI_for_O0

theorem toy_exists_LC_not_CI_global : exists_LC_not_CI := by
  exact Exists.intro O0 toy_exists_LC_not_CI_for_O0

theorem toy_strict_inclusion_possible : ProperSubdomainExists := by
  exact exists_LC_not_CI_implies_proper_subdomain_exists toy_exists_LC_not_CI_global

end FrC
