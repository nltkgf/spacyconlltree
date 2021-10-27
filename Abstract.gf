abstract Abstract = {

	flags
		startcat = UDS ;

	cat
		acl ;
		aclRelcl ;
		advcl ;
		advmod ;
		advmodEmph ;
		advmodLmod ;
		amod ;
		appos ;
		aux ;
		auxPass ;
		case_ ;
		cc ;
		ccPreconj ;
		ccomp ;
		clf ;
		compound ;
		compoundLvc ;
		compoundPrt ;
		compoundRedup ;
		compoundSvc ;
		conj ;
		cop ;
		csubj ;
		csubjPass ;
		dep ;
		det ;
		detNumgov ;
		detNummod ;
		detPoss ;
		discourse ;
		dislocated ;
		expl ;
		explImpers ;
		explPass ;
		explPv ;
		fixed ;
		flat ;
		flatForeign ;
		flatName ;
		goeswith ;
		iobj ;
		list ;
		mark ;
		nmod ;
		nmodPoss ;
		nmodTmod ;
		nsubj ;
		nsubjPass ;
		nummod ;
		nummodGov ;
		obj ;
		obl ;
		oblAgent ;
		oblArg ;
		oblLmod ;
		oblTmod ;
		orphan ;
		parataxis ;
		punct ;
		reparandum ;
		root ;
		vocative ;
		xcomp ;

	 -- coercion funs

	fun
		acl_ : X -> acl ;
		aclRelcl_ : X -> aclRelcl ;
		advcl_ : X -> advcl ;
		advmod_ : X -> advmod ;
		advmodEmph_ : X -> advmodEmph ;
		advmodLmod_ : X -> advmodLmod ;
		amod_ : X -> amod ;
		appos_ : X -> appos ;
		aux_ : X -> aux ;
		auxPass_ : X -> auxPass ;
		case__ : X -> case_ ;
		cc_ : X -> cc ;
		ccPreconj_ : X -> ccPreconj ;
		ccomp_ : X -> ccomp ;
		clf_ : X -> clf ;
		compound_ : X -> compound ;
		compoundLvc_ : X -> compoundLvc ;
		compoundPrt_ : X -> compoundPrt ;
		compoundRedup_ : X -> compoundRedup ;
		compoundSvc_ : X -> compoundSvc ;
		conj_ : X -> conj ;
		cop_ : X -> cop ;
		csubj_ : X -> csubj ;
		csubjPass_ : X -> csubjPass ;
		dep_ : X -> dep ;
		det_ : X -> det ;
		detNumgov_ : X -> detNumgov ;
		detNummod_ : X -> detNummod ;
		detPoss_ : X -> detPoss ;
		discourse_ : X -> discourse ;
		dislocated_ : X -> dislocated ;
		expl_ : X -> expl ;
		explImpers_ : X -> explImpers ;
		explPass_ : X -> explPass ;
		explPv_ : X -> explPv ;
		fixed_ : X -> fixed ;
		flat_ : X -> flat ;
		flatForeign_ : X -> flatForeign ;
		flatName_ : X -> flatName ;
		goeswith_ : X -> goeswith ;
		iobj_ : X -> iobj ;
		list_ : X -> list ;
		mark_ : X -> mark ;
		nmod_ : X -> nmod ;
		nmodPoss_ : X -> nmodPoss ;
		nmodTmod_ : X -> nmodTmod ;
		nsubj_ : X -> nsubj ;
		nsubjPass_ : X -> nsubjPass ;
		nummod_ : X -> nummod ;
		nummodGov_ : X -> nummodGov ;
		obj_ : X -> obj ;
		obl_ : X -> obl ;
		oblAgent_ : X -> oblAgent ;
		oblArg_ : X -> oblArg ;
		oblLmod_ : X -> oblLmod ;
		oblTmod_ : X -> oblTmod ;
		orphan_ : X -> orphan ;
		parataxis_ : X -> parataxis ;
		punct_ : X -> punct ;
		reparandum_ : X -> reparandum ;
		root_ : X -> root ;
		vocative_ : X -> vocative ;
		xcomp_ : X -> xcomp ;

	fun
		root_advcl_det_compound_amod_advcl : root -> advcl -> det -> compound -> amod -> advcl -> UDS ;
	--when there is a data breach, the organisation much check if it needs to notify ;

		root_advcl_nsubjPass_auxPass : root -> advcl -> nsubjPass -> auxPass -> UDS ;
	--if the data breach is within an organisation, no notice is required ;

		root_advcl_nsubj_aux_advcl : root -> advcl -> nsubj -> aux -> advcl -> UDS ;
	--when an organisation knows of a data breach, it must check whether it is a notifiable breach ;

		root_advcl_nsubj_aux_advmod_obj : root -> advcl -> nsubj -> aux -> advmod -> obj -> UDS ;
	--when there is a data breach, the data intermediary must immediately notify the organisation ;

		root_advcl_nsubj_aux_ccomp : root -> advcl -> nsubj -> aux -> ccomp -> UDS ;
	--when an organisation is notified of a data breach, it must assess whether it is a notifiable breach ;

		root_advcl_nsubj_aux_obj_advmod_conj : root -> advcl -> nsubj -> aux -> obj -> advmod -> conj -> UDS ;
	--Where an organisation assesses, in accordance with section 26C, that a data breach is a notifiable data breach, the organisation must notify the Commission as soon as is practicable, but in any case no later than 3 calendar days after the day the organisation makes that assessment. ;

		root_advcl_nsubj_aux_obl_obj : root -> advcl -> nsubj -> aux -> obl -> obj -> UDS ;
	--where an organisation has reason to believe that a data breach affecting personal data in its possession or under its control has occurred, the organisation must conduct, in a reasonable and expeditious manner, an assessment of whether the data breach is a notifiable data breach. ;

		root_advcl_nsubj_conj : root -> advcl -> nsubj -> conj -> UDS ;
	--if significant harm to the affected individual is unlikely, the organisation need not notify the persons ;

		root_advcl_nsubj_cop : root -> advcl -> nsubj -> cop -> UDS ;
	--if it harms the affected individual, the data breach is notifiable ;

		root_advcl_nsubj_cop_case_amod_nmod : root -> advcl -> nsubj -> cop -> case_ -> amod -> nmod -> UDS ;
	--if the data breach affects at least 500 people, it is of significant scale for notification ;

		root_advcl_nsubj_cop_det_amod : root -> advcl -> nsubj -> cop -> det -> amod -> UDS ;
	--if the data breach affects at least 500 people, it is a notifiable breach ;

		root_advcl_nsubj_xcomp : root -> advcl -> nsubj -> xcomp -> UDS ;
	--although the organisation must still notify the Commission, it need not notify the affected individual if it can take rectifiable actions that prevents significant harm to the persons ;

		root_det_compound_nmod_parataxis : root -> det -> compound -> nmod -> parataxis -> UDS ;
	--the organisation must, upon notification by the data intermediary, conduct an assessment of whether the data breach is a notifiable data breach ;

		root_mark_nsubj_nsubj_xcomp : root -> mark -> nsubj -> nsubj -> xcomp -> UDS ;
	--if the organisation implemented technological measure that renders it unlikely that the notifiable data breach will result in significant harm to the affected individual, it need not notify the individuals. ;

		root_nsubjPass_auxPass_advmod_advcl : root -> nsubjPass -> auxPass -> advmod -> advcl -> UDS ;
	--Notification is not required if the data breach is within an organisation ;

		root_nsubjPass_auxPass_advmod_xcomp : root -> nsubjPass -> auxPass -> advmod -> xcomp -> UDS ;
	--a data breach within an organisation is deemed not to be a notifiable data breach ;

		root_nsubjPass_auxPass_xcomp : root -> nsubjPass -> auxPass -> xcomp -> UDS ;
	--data breach of prescribed personal data is deemed to result in significant harm ;

		root_nsubjPass_aux_auxPass : root -> nsubjPass -> aux -> auxPass -> UDS ;
	--every individual affected by the data breach should be notified ;

		root_nsubjPass_aux_auxPass_obl_advmod : root -> nsubjPass -> aux -> auxPass -> obl -> advmod -> UDS ;
	--the Commission must be notified of the data breach as soon as practicable once the organisation assesses it to be a notifiable breach ;

		root_nsubjPass_aux_auxPass_obl_conj : root -> nsubjPass -> aux -> auxPass -> obl -> conj -> UDS ;
	--The notification under subsection (1) must be made in the form and submitted in the manner required by the Commission ;

		root_nsubjPass_aux_auxPass_obl_obl_advcl : root -> nsubjPass -> aux -> auxPass -> obl -> obl -> advcl -> UDS ;
	--the Commission must be notified of the data breach within 3 days once the organisation assesses it to be a notifiable breach ;

		root_nsubjPass_aux_auxPass_obl_obl_advmod : root -> nsubjPass -> aux -> auxPass -> obl -> obl -> advmod -> UDS ;
	--the Commission must be notified of the data breach within 3 days or as soon as practicable once the organisation assesses it to be a notifiable breach ;

		root_nsubj_aux_advmod_obj_advcl : root -> nsubj -> aux -> advmod -> obj -> advcl -> UDS ;
	--the organisation must not notify the affected individual if a prescribed law enforcement agency so instructs ;

		root_nsubj_aux_obj_conj_parataxis : root -> nsubj -> aux -> obj -> conj -> parataxis -> UDS ;
	--the organisation must notify the Commission or affected individual, all the information that is prescribed for this purpose ;

		root_nsubj_aux_obj_obl_advmod_advcl : root -> nsubj -> aux -> obj -> obl -> advmod -> advcl -> UDS ;
	--an organisation must report the notifiable data breach to the Commission as soon as practicable ;

		root_nsubj_aux_obj_obl_obl : root -> nsubj -> aux -> obj -> obl -> obl -> UDS ;
	--an organisation must report the notifiable data breach to the Commission within 3 days of the assessment ;

		root_nsubj_cop : root -> nsubj -> cop -> UDS ;
	--once it is likely to be of significant scale, the data breach is notifiable ;

		root_nsubj_cop_aclRelcl : root -> nsubj -> cop -> aclRelcl -> UDS ;
	--a data intermediary is one that is processing personal data on behalf of and for the purposes of another organisation ;

		root_nsubj_cop_advcl_conj : root -> nsubj -> cop -> advcl -> conj -> UDS ;
	--A data breach is notifiable if it results in, or is likely to result in, significant harm to an affected individual; ;

		root_nsubj_cop_det_aclRelcl : root -> nsubj -> cop -> det -> aclRelcl -> UDS ;
	--The affected individual is the person whose personal data is affected by the data breach. ;

		root_nsubj_cop_det_amod_advcl : root -> nsubj -> cop -> det -> amod -> advcl -> UDS ;
	--a data breach is a notifiable breach if it falls outside the organisation ;

		root_nsubj_cop_det_amod_compound : root -> nsubj -> cop -> det -> amod -> compound -> UDS ;
	--a data breach affecting more than 500 people is a notifiable data breach ;

		root_nsubj_cop_det_amod_conj_conj_conj_conj_conj_conj : root -> nsubj -> cop -> det -> amod -> conj -> conj -> conj -> conj -> conj -> conj -> UDS ;
	--Data breach is the unauthorised access, collection, use, disclosure, copying, modification or disposal of personal data ;

		root_nsubj_cop_det_nmod : root -> nsubj -> cop -> det -> nmod -> UDS ;
	--Data breach is the loss of any storage medium or device on which personal data is stored in circumstances where the unauthorised access, collection, use, disclosure, copying, modification or disposal of the personal data is likely to occur. ;

		root_nsubj_cop_obl_parataxis : root -> nsubj -> cop -> obl -> parataxis -> UDS ;
	--once an organisation is aware of a data breach, it must assess if it is a notifiable breach ;

		root_nsubj_obj : root -> nsubj -> obj -> UDS ;
	--The PDPA covers personal data stored in electronic and non-electronic formats. ;

		root_nsubj_obj_advcl : root -> nsubj -> obj -> advcl -> UDS ;
	--The Commission may, on the written application of an organisation, waive the requirement to notify an affected individual as it thinks fit ;

		root_nsubj_obl : root -> nsubj -> obl -> UDS ;
	--significant harm refers to data breach of any prescribed personal data or class of personal data of the individual ;

}